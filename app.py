from flask import Flask, jsonify, request
from firebase_auth import check_auth
from predict import preprocess_image_from_url, make_prediction

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({'message': 'Hello, from Makara!'}), 200


@app.route('/playground/protected-endpoint')
@check_auth
def protected_route(decoded_token):
    # You can now use the decoded_token which contains the user information
    user_id = decoded_token['uid']
    return jsonify({'message': f'Hello, user {user_id}'})

@app.route('/predict', methods=['POST'])
@check_auth
def predict(decoded_token):
    data = request.json

    # Check if the image URL is provided
    if not data or 'image_url' not in data:
        return jsonify({'status': 'error', 'message': 'No image URL provided'}), 400

    image_url = data['image_url']


    try:
        # Preprocess the image from the URL
        img_array = preprocess_image_from_url(image_url)

        # Make prediction
        class_label = make_prediction(img_array)

        return jsonify({
            "status": {
                "code": 200,
                "message": "Success predicting"
            },
            "data": {
                "name": class_label,
            }
        }), 200

    except Exception as e:
        print(f"Error: {e}")
        if "Failed to download image" in str(e):
            status_code = 400
        elif "URL does not point to a valid image" in str(e):
            status_code = 415  # Unsupported Media Type
        else:
            status_code = 500  # Internal Server Error

        return jsonify({'status': 'error', 'message': str(e)}), status_code


if __name__ == '__main__':
    app.run(debug=True)
    