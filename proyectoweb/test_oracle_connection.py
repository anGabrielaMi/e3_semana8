import oracledb

# Inicializa el cliente Oracle con el wallet
oracledb.init_oracle_client(config_dir=r"C:\Wallet_AMmodelamiento25")  # ←ruta

# Intenta conectar
try:
    connection = oracledb.connect(
        user="ficciona",
        password="proyectoWeb2025sep",
        dsn="ammodelamiento25_tpurgent"  # ← alias definido en tnsnames.ora
    )
    print("✅ Conexión exitosa")
    print("Versión de Oracle:", connection.version)
    connection.close()
except Exception as e:
    print("❌ Error al conectar:")
    print(e)