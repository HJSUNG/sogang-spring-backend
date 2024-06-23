from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import datetime
import pytz
import pymysql

from app.sentiment_analysis.bert import sentiment_analysis
from app.crawling.crawl_weather import crawl_weather_info

common_blueprint = Blueprint('common', __name__, url_prefix='/api/common')


@common_blueprint.route('getWeatherInfo', methods=['POST'])
def get_weather_info():
    weather_info = crawl_weather_info()

    return jsonify({
        "stacd": 100,
        "weather_info": weather_info
    }), 200


@common_blueprint.route('textSentimentAnalysis', methods=['POST'])
@jwt_required()
def text_sentiment_analysis():
    current_user = get_jwt_identity()
    db_config = current_app.config['DB_CONFIG']

    kst = pytz.timezone('Asia/Seoul')
    now = datetime.now(kst)

    data = request.get_json()

    text = data['inputText']

    analysis_result = sentiment_analysis(text)

    print(analysis_result)

    try:
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        query = """
                INSERT INTO TB_TEXT_SENTIMENT_ANALYSIS 
                VALUES (%s,%s,%s,%s,%s,%s)
                """

        cursor.execute(query, (current_user["USER_ID"], now.strftime("%Y-%m-%d %H:%M:%S"), text, analysis_result[0], analysis_result[1],analysis_result[2]))

        connection.commit()
        cursor.close()

        return jsonify({
            "stacd": 100,
            "analysis_result": analysis_result
        }), 200

    except Exception as e:
        return jsonify({'error': e})

    finally:
        connection.close()