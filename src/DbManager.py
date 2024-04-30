import pandas as pd
import psycopg2
import json
import datetime
import yfinance as yf




class DbManager:
    
    def __init__(self, esquema = None):
        config = self.cargar_configuracion()
        self.dbname = config["database"]
        self.user = config["user"]
        self.password = config["password"]
        self.host = config["host"]
        self.port = config["port"]
        self.esquema = esquema or config["scheme"]
        self.connection = None
        self.connection = self.connect()
        for key, value in config.items():
            print(f'{key}: {value}')

    def cargar_configuracion(self):
        with open('config/postgres.json') as f:
            config = json.load(f)
        return config['postgres']

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            #print("Conexión exitosa a la base de datos PostgreSQL")
            return True
        except (Exception, psycopg2.Error) as error:
            print("Error al conectar a la base de datos PostgreSQL:", error)
            assert error
            


    def create_table(self, table_name, columns):
        try:
            cursor = self.connection.cursor()
            consulta = f"CREATE TABLE IF NOT EXISTS {self.esquema}.{table_name} ({columns});"
            cursor.execute(consulta)
            self.connection.commit()
            print(f"Tabla '{self.esquema}.{table_name}' creada exitosamente.")
            cursor.close()
        except (Exception, psycopg2.Error) as error:
            print("Error al crear la tabla:", error)

    def insert_values(self, nombre_tabla, valores):
        try:
            cursor = self.connection.cursor()
            
            valores = ', '.join([f"'{val}'" for val in valores])

            consulta = f"INSERT INTO {self.esquema}.{nombre_tabla} VALUES ({valores});"
            cursor.execute(consulta)
            self.connection.commit()
            print(f"Valores agregados a la tabla '{self.esquema}.{nombre_tabla}' exitosamente.")
            cursor.close()
        except (Exception, psycopg2.Error) as error:
            print("Error al agregar valores:", error)


    def add_individual_share(self, nombre_tabla: str = "shares", valores: list = []):
        """_summary_

        Args:
            nombre_tabla (_type_): 
                Nombre de la tabla:
                    - company, shares...
            valores (list): 
                Lista de valores a añadir:
                    - company_code: string
                    - date: datetime
                    - open: float
                    - High: float
                    - Low: flaot
                    - close: float
                    - Adj Close: float
                    - volume: integer
        """   
        
        try:
            valores, flag = self._check_data(valores)
            if flag:
                cursor = self.connection.cursor()
                
                valores = ', '.join([f"'{val}'" for val in valores])
                print(valores)
                consulta = f"INSERT INTO {self.esquema}.{nombre_tabla} VALUES ({valores});"
                cursor.execute(consulta)
                
                #self.connection.autocommit(True)
                self.connection.commit()
                print(f"Valores agregados a la tabla '{self.esquema}.{nombre_tabla}' exitosamente.")
                cursor.close()
        except (Exception, psycopg2.Error) as error:
            print("Error al agregar valores:", error)

    def add_company(self, nombre_tabla: str = "company", valores: list = []):
        """_summary_

        Args:
            nombre_tabla (_type_): 
                Nombre de la tabla:
                    - company, shares...
            valores (list): 
                Lista de valores a añadir:
                    - company_code: string
                    - company_name: string
                    - markey: string
        """   
        self.connect()
        try:
            valores, flag = self._check_data(valores, table = "company")
            if flag:
                cursor = self.connection.cursor()
                
                valores = ', '.join([f"'{val}'" for val in valores])
                print(valores)
                consulta = f"INSERT INTO {self.esquema}.{nombre_tabla} VALUES ({valores});"
                cursor.execute(consulta)
                
                #self.connection.autocommit(True)
                self.connection.commit()
                print(f"Valores agregados a la tabla '{self.esquema}.{nombre_tabla}' exitosamente.")
                cursor.close()
                self.close_conexion()
        except (Exception, psycopg2.Error) as error:
            print("Error al agregar valores:", error)

    def get_all_tickers(self):
        """_summary_
            get a list with all the tickers 
        Args:
            No Args
        """
        
        self.connect()
        cursor = self.connection.cursor()
        
        # consulta = f"SELECT COLUMN_NAME
        #             FROM INFORMATION_SCHEMA.COLUMNS
        #             WHERE TABLE_SCHEMA = '{self.esquema}'
        #             AND TABLE_NAME = '{table_name}';"
        
        consulta = f"""
            SELECT company_code
            FROM {self.esquema}.company
            """

        cursor.execute(consulta)
        
        columns = cursor.fetchall() #result será una lista con los datos de la query
        
        # Rearrenge format
        columns = [column[0] for column in columns]
        
        self.connection.commit()

        self.close_conexion()

        return columns 


    def get_tickers_from_market(self, market: str):
        """_summary_
            get a list with all the tickers from a certain market
        Args:
            market (str): "AEX", "IBEX35"...
        """
        
        self.connect()
        cursor = self.connection.cursor()
        
        # consulta = f"SELECT COLUMN_NAME
        #             FROM INFORMATION_SCHEMA.COLUMNS
        #             WHERE TABLE_SCHEMA = '{self.esquema}'
        #             AND TABLE_NAME = '{table_name}';"
        
        consulta = f"""
            SELECT company_code
            FROM {self.esquema}.company
            WHERE market = '{market}'
            """

        cursor.execute(consulta)
        
        columns = cursor.fetchall() #result será una lista con los datos de la query
        
        # Rearrenge format
        columns = [column[0] for column in columns]
        
        self.connection.commit()

        self.close_conexion()

        return columns 

    def download_add_bbdd_company(self, company: str):
        df = self.get_historical_data_yf_df(company=company)
        self.add_df_to_postgresql(df=df, company_str=company)
        return df        

    def add_df_to_postgresql(self, df, company_str: str):
        
        result = []
        # Conectar a la base de datos
        #db = PostgreSQLDB("dbo")
        #db.conectar()
        #print("conntected")
        #for i in range(len(df)):
        self.connect()
        for index, df in df.iterrows():        
            """
                cada linea del df tendrá que lanzar la query de añadir dato
            """
            try:
                if isinstance(df["Date"], pd.Timestamp):
                    # df["Date"] = df["Date"].strftime("%Y-%m-%d")  # Convertir Timestamp a cadena
                    df["Date"] = df["Date"].to_pydatetime()
                    #print(df)
                    date = df["Date"]
                    #print(type(date))
                    # date = df["Date"].date()
                else:
                    date = datetime.datetime.strptime(df["Date"], "%Y-%m-%d")
                #print(date)
                values = [company_str, date, float(df["Open"]), float(df["High"]), float(df["Low"]), float(df["Close"]), float(df["Adj Close"]), int(df["Volume"])]
                #print(values)
                #print(self._check_data(values))
                values, flag = self._check_data(values)
                #print(values)
                #print(flag)
                if flag:
                #if _check_data(values):
                    
                    #print("data is correct")
                    # Si el dato (lista) es valido, se puede mandar a la bbdd:  
                    # Agregar valores a la tabla
                    self.add_individual_share(nombre_tabla="shares", valores=values)
                    #print('Data added correctly.')
                    result.append(values)
            except Exception as e:
                print("Error ocurred: " + str(e))
                
        self.close_conexion()
        return result


    def get_historical_data_yf_df(self, company, begin = '1980-01-20', end = '2024-01-20'):
        # Obtener datos históricos para el índice AEX para la fecha actual
        df = yf.download(company, start=begin, end = end)

        # Verificar si se obtuvieron datos para el día actual
        if not df.empty:
            # Mostrar los datos más importantes
            df.reset_index(inplace=True, drop=False)
            return df
        else:
            assert 'No hay ningun dato entre esas fechas.'



    def _check_data(self, valores, table="shares"):
        if table == "shares":
            # Verificar que la lista de valores tenga el formato correcto
            if len(valores) != 8:
                print("Error: La lista 'valores' debe contener exactamente 7 elementos.")
                """
                Lista de valores a añadir:        
                    - company_code: string
                    - date: datetime
                    - open: float
                    - High: float
                    - Low: flaot
                    - close: float
                    - Adj Close: float
                    - volume: integer
                """
                return valores, False

            # Desempaquetar los valores de la lista
            company_code, date, open_val, high_val, low_val, close_val, adj_close, volume = valores

            # Verificar que los valores estén en el formato correcto
            if not isinstance(company_code, str):
                print("Error: 'company_code' debe ser una cadena de caracteres.")
                return valores, False
            #if not isinstance(date, datetime.date):
            #    print("Error: 'date' debe ser un objeto de fecha.")
            if not isinstance(date, datetime.date):
                print("Error: 'date' debe ser un objeto de fecha.")
                if isinstance(date, datetime.datetime.timestamp):
                    date_str = valores["Date"].strftime("%Y-%m-%d")  # Convertir Timestamp a cadena
                    return date_str, True
                return valores, False
                #return valores, False
                
            if open_val is not None and not isinstance(open_val, (int, float)):
                print("Error: 'open_val' debe ser un número entero o de punto flotante.")
                return valores, False
            if high_val is not None and not isinstance(high_val, (int, float)):
                print("Error: 'high_val' debe ser un número entero o de punto flotante.")
                return valores, False
            if low_val is not None and not isinstance(low_val, (int, float)):
                print("Error: 'low_val' debe ser un número entero o de punto flotante.")
                return valores, False
            if close_val is not None and not isinstance(close_val, (int, float)):
                print("Error: 'close_val' debe ser un número entero o de punto flotante.")
                return valores, False
            if adj_close is not None and not isinstance(adj_close, (int, float)):
                print("Error: 'adj_close' debe ser un número entero o de punto flotante.")
                return valores, False
            if volume is not None and not isinstance(volume, int):
                print("Error: 'volume' debe ser un número entero.")
                return valores, False
            else:
                print("data in correct format")
                return valores, True
        elif table == "company":
            # Desempaquetar los valores de la lista
            company_code, company_name, market = valores

            # Verificar que los valores estén en el formato correcto
            if not isinstance(company_code, str):
                print("Error: 'company_code' debe ser una cadena de caracteres.")
                return valores, False
            if not isinstance(company_name, str):
                print("Error: 'company_name' debe ser una cadena de caracteres.")
                return valores, False
            if not isinstance(market, str):
                print("Error: 'market' debe ser una cadena de caracteres.")
                return valores, False
            else:
                print("data in correct format")
                return valores, True

    def close_conexion(self):
        if self.connection:
            self.connection.close()
            print("Conexión cerrada correctamente.")

    ### Querys desde python para obtener info
    
    def get_all_shares(self, table_name: str = "shares", dataframe = True):
        """
            Query to retrieve all the data from the shares table 
            
                - Dataframe: Bool. Indica si quieres los datos en formato df
        """
        self.connect()
        cursor = self.connection.cursor()
        consulta = f"SELECT * FROM  {self.esquema}.{table_name};"
        cursor.execute(consulta)
        
        result = cursor.fetchall() #result será una lista con los datos de la query
        
        # format to dataframe
        if dataframe:
            columns = self.get_columns_name("shares")
            df = pd.DataFrame(result, columns=columns)
        
        #self.connection.commit()

        self.close_conexion()
         
        return df
    
    def get_columns_name(self, table_name: str = "shares") -> list:
        """
            Query get columns list from table
        """
        
        self.connect()
        cursor = self.connection.cursor()
        
        # consulta = f"SELECT COLUMN_NAME
        #             FROM INFORMATION_SCHEMA.COLUMNS
        #             WHERE TABLE_SCHEMA = '{self.esquema}'
        #             AND TABLE_NAME = '{table_name}';"
        
        consulta = f"""
            SELECT COLUMN_NAME
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = '{self.esquema}'
            AND TABLE_NAME = '{table_name}';
            """

        cursor.execute(consulta)
        
        columns = cursor.fetchall() #result será una lista con los datos de la query
        
        # Rearrenge format
        columns = [column[0] for column in columns]
        
        self.connection.commit()

        self.close_conexion()

        return columns

    def fetch_to_df(self, result: list) -> pd.DataFrame():
        """ 
            Converts bbdd list data in pandas dataframe
            result será una lista con los datos de la query
        """
        columns = self.get_columns_name("shares")
        df = pd.DataFrame(result, columns=columns)
        return df