# src/HiTrustHandler/app/main.py
import sys
import os
import pandas as pd

from flask import Flask, render_template, request, jsonify
from ansi2html import Ansi2HTMLConverter


class hitrust_handler():

    def __init__(self):
        self.app = Flask(__name__)
        self.dmh_session = None
        self.add_routes()

    def add_routes(self):
        @self.app.route('/')
        def index():
            return render_template('index.html')

        @self.app.route('/get_log')
        def get_log():
            log_file_path = get_log_file_path()
            with open(log_file_path, 'r') as log_file:
                log_content = log_file.read()
            conv = Ansi2HTMLConverter()
            html_content = conv.convert(log_content, full=True)

            return html_content

        @self.app.route('/login', methods=['POST'])
        def login():
            data = request.json
            username = data.get('username')
            password = data.get('password')

            logger.info(f'Start login process with username `{username}`')

            self.dmh_session = dmh_session(username, password)
            if self.dmh_session.is_signed:
                return jsonify({'status': 'success'})
            else:
                return jsonify({'status': 'fail'})

        @self.app.route('/submit_source', methods=['POST'])
        def submit_source():
            data = request.json
            remote_folder = data.get('source').rstrip()
            # Download the remote file from the source address to local temp folder
            copy_file_to_local(remote_folder)
            local_folder = get_cache_directory()
            # Covert all .xlsx files in the local folder into json format data and output it in `output.json`
            parser = hi_trust_parser(local_folder)
            all_jdata = parser.get_json_data()
            return jsonify({'status': 'success', 'task_data': all_jdata})

        @self.app.route('/get_cusip', methods=['POST'])
        def get_cusip():
            data = request.json
            fund_code = data.get('name')
            UR_code = data.get('ur')
            component_data = data.get('data')
            ex_date = data.get('ex_date')
            DPU = data.get('dpu')
            cusip, investment_status = 'Not Found', 'Not Found'
            cusip_UR_list = self.dmh_session.dmh_filter(Fund=fund_code)
            if cusip_UR_list:
                for cusip_UR_dict in cusip_UR_list:
                    if cusip_UR_dict['UR_code'] == UR_code:
                        cusip = cusip_UR_dict['cusip']
                        investment_status = cusip_UR_dict['investment_status']
            if investment_status != 'Not Found' and cusip != 'Not Found':
                parser = hi_trust_parser()
                res = self.dmh_session.get_mr_data_detail(Asset_ID=cusip, Ex_Date=ex_date)
                mr_data, row_id = res['cv_dict'], res['row_id']
                if abs(float(mr_data['MCH_NET_INCM_DPU_RT']) - DPU) / DPU > 0.01:
                    return jsonify({'status': 'fail', 'cusip': cusip, 'investment_status': investment_status})
                cv_dict = parser.parse_component(fund_type=investment_status, component_data=component_data,
                                                 mr_data=mr_data)
                self.dmh_session.post_change(MR_data_cv_dict=cv_dict, row_id=row_id)
            return jsonify({'status': 'success', 'cusip': cusip, 'investment_status': investment_status})


if __name__ == '__main__':
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from dmh_handler.dmh_session import dmh_session
    from source_file_handler.parser import hi_trust_parser
    from utils.helpers import copy_file_to_local, get_cache_directory
    from utils.logger import get_log_file_path, logger, log_exception

    hitrust_handler = hitrust_handler()
    hitrust_handler.app.run(debug=True)
