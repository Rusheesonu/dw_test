from flask import Flask, jsonify, render_template, request
import psycopg2
import os

app = Flask(__name__, template_folder='templates')

# Establish connection to your PostgreSQL database
def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv('POSTGRES_DB'),
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD'),
            host=os.getenv('POSTGRES_HOST'),
            port=os.getenv('POSTGRES_PORT')
        )
        print(conn)
        if conn:
            print("connection sucesss")
        return conn 
    except psycopg2.OperationalError as e:
        # Catching connection-related errors
        print(f"Operational error: {e}")
        raise  # Re-raise the exception to handle it elsewhere or terminate
    except psycopg2.DatabaseError as e:
        # Catching generic database errors
        print(f"Database error: {e}")
        raise  # Re-raise the exception to handle it elsewhere or terminate
    except Exception as e:
        # Catching other unexpected errors
        print(f"An unexpected error occurred: {e}")
        raise  # Re-raise the exception to handle it elsewhere or terminate

# Endpoint to retrieve all data from the TrackedProducts table
@app.route('/products', methods=['GET'])
def get_products():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM dw_test_table")
        data = cursor.fetchall()

        conn.close()

        return jsonify({'products': data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint to compute availability score
@app.route('/availability-score', methods=['GET'])
def get_availability_score():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM dw_test_table")
        total_products = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM dw_test_table WHERE stock = 'In Stock'")
        in_stock_products = cursor.fetchone()[0]

        availability_score = in_stock_products / total_products if total_products != 0 else 0

        conn.close()

        return jsonify({
            'availability_score': availability_score,
            'in_stock_products': in_stock_products,
            'total_tracked_products': total_products
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Endpoint to render the view page
@app.route('/view', methods=['GET'])
def view_products():
    return render_template('view_products.html')

# Endpoint to handle product search
@app.route('/search', methods=['GET'])
def search_products():
    try:
        search_query = request.args.get('query')

        conn = get_db_connection()
        cursor = conn.cursor()

        # Query based on the 'meta_info' column for the reference_product_id
        cursor.execute("""
            SELECT meta_info, available_price, stock, source 
            FROM dw_test_table 
            WHERE meta_info->>'reference_product_id' = %s
        """, (search_query,))

        data = cursor.fetchall()

        conn.close()

        return jsonify({'products': data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Endpoint to filter in-stock products
@app.route('/instock', methods=['GET'])
def filter_instock_products():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM dw_test_table WHERE stock = 'In Stock'")
        data = cursor.fetchall()

        conn.close()

        return jsonify({'in_stock_products': data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True ,port=8000, host='0.0.0.0')
