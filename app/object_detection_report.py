from flask import Blueprint, jsonify, request, current_app
from datetime import datetime
import pytz
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import pymysql

from app.llm.chat_gpt import chat_gpt_query

objectDetectionReport_blueprint = Blueprint('objectDetectionReport', __name__, url_prefix='/api/objectDetectionReport')

@objectDetectionReport_blueprint.route('getReportData', methods=['POST'])
@jwt_required()
def get_report_data():
    current_user = get_jwt_identity()
    db_config = current_app.config['DB_CONFIG']

    try:
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        text_sentiment_analysis_query = """
            SELECT USER_ID,TEXT, ANALYSIS_RESULT, POSITIVE_SCORE, NEGATIVE_SCORE,DATE_FORMAT(ANALYSIS_DTTM, '%%Y-%%m-%%d %%H:%%i:%%s') AS ANALYSIS_DTTM
            FROM TB_TEXT_SENTIMENT_ANALYSIS ttsa 
            WHERE ttsa.USER_ID = %s
            ORDER BY ANALYSIS_DTTM DESC
            LIMIT 1
            """

        cursor.execute(text_sentiment_analysis_query, (current_user["USER_ID"]))
        text_sentiment_analysis_result = cursor.fetchall()

        normal_test_query = """
            SELECT DETECTION_NO,USER_ID,TEST_TP,DATE_FORMAT(START_DTTM, '%%Y-%%m-%%d %%H:%%i:%%s') AS START_DTTM, DATE_FORMAT(END_DTTM, '%%Y-%%m-%%d %%H:%%i:%%s') AS END_DTTM 
            FROM TB_DETECTION_MASTER tdm 
            WHERE tdm.USER_ID = %s AND TEST_TP = "normal"
            ORDER BY DETECTION_NO DESC
            LIMIT 1
            """

        cursor.execute(normal_test_query, (current_user["USER_ID"]))
        normal_test_result = cursor.fetchall()

        normal_test_detail_query = """
            SELECT t1.TEST_TP, t1.DETECTION_TP, t1.DETECTION_TP_CLASS,  IFNULL(t2.COUNTING,0) as COUNTING
            FROM 
                (SELECT TMDTC.DETECTION_TP, TMDTC.DETECTION_TP_CLASS, TMDT.TEST_TP
                FROM TB_MST_DETECTION_TP_CLASS TMDTC
                LEFT JOIN TB_MST_DETECTION_TP TMDT ON TMDTC.DETECTION_TP =TMDT.DETECTION_TP 
                WHERE TMDT.TEST_TP = 'normal') t1
                LEFT JOIN 
                    (SELECT tdd.DETECTION_NO, tdm.TEST_TP, tdd.DETECTION_TP, tdd.DETECTION_TP_CLASS,count(*) as COUNTING
                    FROM TB_DETECTION_DETAIL tdd 
                    LEFT JOIN TB_DETECTION_MASTER tdm ON tdd.DETECTION_NO = tdm.DETECTION_NO 
                    WHERE tdm.DETECTION_NO = (SELECT DETECTION_NO 
                        FROM TB_DETECTION_MASTER tdm 
                        WHERE tdm.USER_ID = %s AND TEST_TP = 'normal'
                        ORDER BY DETECTION_NO DESC
                        LIMIT 1)
                    GROUP BY tdm.TEST_TP, tdd.DETECTION_TP, tdd.DETECTION_TP_CLASS ) t2 ON (t1.TEST_TP = t2.TEST_TP AND t1.DETECTION_TP = t2.DETECTION_TP AND t1.DETECTION_TP_CLASS = t2.DETECTION_TP_CLASS)
            """

        cursor.execute(normal_test_detail_query, (current_user["USER_ID"]))
        normal_test_detail_result = cursor.fetchall()

        sleeping_test_query = """
                    SELECT DETECTION_NO,USER_ID,TEST_TP,DATE_FORMAT(START_DTTM, '%%Y-%%m-%%d %%H:%%i:%%s') AS START_DTTM, DATE_FORMAT(END_DTTM, '%%Y-%%m-%%d %%H:%%i:%%s') AS END_DTTM 
                    FROM TB_DETECTION_MASTER tdm 
                    WHERE tdm.USER_ID = %s AND TEST_TP = "sleeping"
                    ORDER BY DETECTION_NO DESC
                    LIMIT 1
                    """

        cursor.execute(sleeping_test_query, (current_user["USER_ID"]))
        sleeping_test_result = cursor.fetchall()

        sleeping_test_detail_query = """
                    SELECT t1.TEST_TP, t1.DETECTION_TP, t1.DETECTION_TP_CLASS,  IFNULL(t2.COUNTING,0) as COUNTING
                    FROM 
                        (SELECT TMDTC.DETECTION_TP, TMDTC.DETECTION_TP_CLASS, TMDT.TEST_TP
                        FROM TB_MST_DETECTION_TP_CLASS TMDTC
                        LEFT JOIN TB_MST_DETECTION_TP TMDT ON TMDTC.DETECTION_TP =TMDT.DETECTION_TP 
                        WHERE TMDT.TEST_TP = 'sleeping') t1
                        LEFT JOIN 
                            (SELECT tdd.DETECTION_NO, tdm.TEST_TP, tdd.DETECTION_TP, tdd.DETECTION_TP_CLASS,count(*) as COUNTING
                            FROM TB_DETECTION_DETAIL tdd 
                            LEFT JOIN TB_DETECTION_MASTER tdm ON tdd.DETECTION_NO = tdm.DETECTION_NO 
                            WHERE tdm.DETECTION_NO = (SELECT DETECTION_NO 
                                FROM TB_DETECTION_MASTER tdm 
                                WHERE tdm.USER_ID = %s AND TEST_TP = 'sleeping'
                                ORDER BY DETECTION_NO DESC
                                LIMIT 1)
                            GROUP BY tdm.TEST_TP, tdd.DETECTION_TP, tdd.DETECTION_TP_CLASS ) t2 ON (t1.TEST_TP = t2.TEST_TP AND t1.DETECTION_TP = t2.DETECTION_TP AND t1.DETECTION_TP_CLASS = t2.DETECTION_TP_CLASS)
                    """

        cursor.execute(sleeping_test_detail_query, (current_user["USER_ID"]))
        sleeping_test_detail_result = cursor.fetchall()

        pose_test_query = """
                            SELECT DETECTION_NO,USER_ID,TEST_TP,DATE_FORMAT(START_DTTM, '%%Y-%%m-%%d %%H:%%i:%%s') AS START_DTTM, DATE_FORMAT(END_DTTM, '%%Y-%%m-%%d %%H:%%i:%%s') AS END_DTTM 
                            FROM TB_DETECTION_MASTER tdm 
                            WHERE tdm.USER_ID = %s AND TEST_TP = "pose"
                            ORDER BY DETECTION_NO DESC
                            LIMIT 1
                            """

        cursor.execute(pose_test_query, (current_user["USER_ID"]))
        pose_test_result = cursor.fetchall()

        pose_test_detail_query = """
                            SELECT t1.TEST_TP, t1.DETECTION_TP, t1.DETECTION_TP_CLASS,  IFNULL(t2.COUNTING,0) as COUNTING
                            FROM 
                                (SELECT TMDTC.DETECTION_TP, TMDTC.DETECTION_TP_CLASS, TMDT.TEST_TP
                                FROM TB_MST_DETECTION_TP_CLASS TMDTC
                                LEFT JOIN TB_MST_DETECTION_TP TMDT ON TMDTC.DETECTION_TP =TMDT.DETECTION_TP 
                                WHERE TMDT.TEST_TP = 'pose') t1
                                LEFT JOIN 
                                    (SELECT tdd.DETECTION_NO, tdm.TEST_TP, tdd.DETECTION_TP, tdd.DETECTION_TP_CLASS,count(*) as COUNTING
                                    FROM TB_DETECTION_DETAIL tdd 
                                    LEFT JOIN TB_DETECTION_MASTER tdm ON tdd.DETECTION_NO = tdm.DETECTION_NO 
                                    WHERE tdm.DETECTION_NO = (SELECT DETECTION_NO 
                                        FROM TB_DETECTION_MASTER tdm 
                                        WHERE tdm.USER_ID = %s AND TEST_TP = 'pose'
                                        ORDER BY DETECTION_NO DESC
                                        LIMIT 1)
                                    GROUP BY tdm.TEST_TP, tdd.DETECTION_TP, tdd.DETECTION_TP_CLASS ) t2 ON (t1.TEST_TP = t2.TEST_TP AND t1.DETECTION_TP = t2.DETECTION_TP AND t1.DETECTION_TP_CLASS = t2.DETECTION_TP_CLASS)
                            """

        cursor.execute(pose_test_detail_query, (current_user["USER_ID"]))
        pose_test_detail_result = cursor.fetchall()


        cursor.close()

        return jsonify({
            "stacd": 100,
            "text_sentiment_analysis": text_sentiment_analysis_result,
            "normal_test": normal_test_result,
            "normal_test_detail": normal_test_detail_result,
            "sleeping_test": sleeping_test_result,
            "sleeping_test_detail": sleeping_test_detail_result,
            "pose_test": pose_test_result,
            "pose_test_detail": pose_test_detail_result,
        }), 200
    except Exception as e:
        return jsonify({'error': e})

    finally:
        connection.close()


@objectDetectionReport_blueprint.route('getLLMResult', methods=['POST'])
@jwt_required()
def get_llm_result():
    current_user = get_jwt_identity()

    data = request.get_json()

    query_text = data['llm_input']
    result_text = ''

    if query_text:
        result_text = chat_gpt_query(query_text)

    if result_text:
        return jsonify({
            "stacd": 100,
            "result_text": result_text
        }), 200
    else:
        return jsonify({
            "stacd": 101,
            "result_text": result_text
        }), 200