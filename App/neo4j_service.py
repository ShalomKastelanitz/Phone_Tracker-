class InsightsRepository:
    def __init__(self, driver):
        self.driver = driver

    def get_bluetooth_connections(self):
        with self.driver.session() as session:
            query = """
                MATCH (start:Device)
                MATCH (end:Device)
                WHERE start <> end
                MATCH path = shortestPath((start)-[:CONNECTED*]->(end))
                WHERE ALL(r IN relationships(path) WHERE r.method = 'Bluetooth')
                WITH path, length(path) as pathLength
                ORDER BY pathLength DESC
                LIMIT 1
                RETURN length(path) as path_length
            """

            result = session.run(query).single()
            if result is None:
                return None
            return result['path_length']

    def get_signal_strength(self):
        with self.driver.session() as session:
            query = """
                MATCH (d1:Device)-[r:CONNECTED]->(d2:Device)
                WHERE r.signal_strength_dbm > -60
                RETURN d1.name as from_name, 
                       d2.name as to_name, 
                       r.signal_strength_dbm as signal_strength
            """

            result = session.run(query)
            if result is None:
                return None

            signals = [{"from": record['from_name'],
                        "to": record["to_name"],
                        "strength": record['signal_strength']}
                       for record in result]
            print(signals)
            return signals

    def get_connected_count(self, device_id):
        with self.driver.session() as session:
            query = """
                MATCH (d1:Device {device_id: $device_id})-[r:CONNECTED]-(d2:Device)
                RETURN COUNT(d2) as connected_count
            """

            result = session.run(query, device_id=device_id).single()
            if result is None:
                return 0
            return result['connected_count']

    def check_connection_status(self, device_id1, device_id2):
        with self.driver.session() as session:
            query = """
                MATCH (d1:Device {device_id: $device_id1})-[r:CONNECTED]-(d2:Device {device_id: $device_id2})
                RETURN d1
            """

            result = session.run(query, device_id1=device_id1, device_id2=device_id2).single()
            return result is not None

    def get_last_interaction(self, device_id):
        with self.driver.session() as session:
            query = """
                MATCH (d1:Device {device_id: $device_id})-[r:CONNECTED]-(d2:Device)
                ORDER BY r.timestamp DESC
                LIMIT 1
                RETURN d2.name as name,
                       r.timestamp as timestamp
            """

            result = session.run(query, device_id=device_id).single()
            if result is None:
                return None
            return {'name': result['name'], 'timestamp': result['timestamp'].isoformat()}
