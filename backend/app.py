from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

def get_db():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "db"),
        database=os.environ.get("DB_NAME", "votacion"),
        user=os.environ.get("DB_USER", "postgres"),
        password=os.environ.get("DB_PASSWORD", "postgres")
    )

@app.route("/votar", methods=["POST"])
def votar():
    data = request.get_json()
    codigo = data.get("codigo")
    candidato_id = data.get("candidato_id")

    if not codigo or not candidato_id:
        return jsonify({"exito": False, "mensaje": "Código y candidato son requeridos"}), 400

    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO votos (codigo, candidato_id) VALUES (%s, %s)",
            (codigo, candidato_id)
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"exito": True, "mensaje": "Voto registrado exitosamente"})
    except psycopg2.errors.UniqueViolation:
        return jsonify({"exito": False, "mensaje": "Este código ya votó anteriormente"}), 409
    except Exception as e:
        return jsonify({"exito": False, "mensaje": str(e)}), 500

# BONUS: endpoint de resultados
@app.route("/resultados", methods=["GET"])
def resultados():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT c.nombre, COUNT(v.candidato_id) as votos
        FROM candidatos c
        LEFT JOIN votos v ON c.id = v.candidato_id
        GROUP BY c.id, c.nombre
        ORDER BY votos DESC
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{"candidato": r[0], "votos": r[1]} for r in rows])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)