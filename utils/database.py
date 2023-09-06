import sqlite3

class DBManager:
    def __init__(
        self,
        db_name:str='data/mpu_bot.db'):
        self.connect = sqlite3.connect(db_name)
        self.cursor = self.connect.cursor()
        self._initialize_tables()

    def _initialize_tables(self):
        """Create tables if they don't exist."""
        # Guild table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Guilds (
            id INTEGER PRIMARY KEY,
            guild_id INTEGER UNIQUE NOT NULL
        )
        ''')

        # ParentChannels table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS ParentChannels (
            id INTEGER PRIMARY KEY,
            guild_id INTEGER,
            parent_channel_id INTEGER UNIQUE NOT NULL,
            name_template TEXT,
            FOREIGN KEY (guild_id) REFERENCES Guilds(guild_id)
        )
        ''')

        # TemporaryChannels table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS TemporaryChannels (
            id INTEGER PRIMARY KEY,
            parent_channel_id INTEGER,
            temporary_channel_id INTEGER UNIQUE NOT NULL,
            FOREIGN KEY (parent_channel_id) REFERENCES ParentChannels(parent_channel_id)
        )
        ''')

        self.connect.commit()

    # --------------------------------------------------------------------------
    # Generic methods

    # HACK : add a proper log function
    def _execute_query(
        self,
        query:str,
        params:tuple
        ) -> bool:
        try:
            self.cursor.execute(query, params)
            self.connect.commit()
            return True
        except sqlite3.IntegrityError:
            print(f"Integrity error: A record with the same unique key already exists.")
            return False
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False

    def _insert(
        self,
        table:str,
        columns:tuple,
        values:tuple
        ) -> bool:
        """
        Insert a new record into the specified table.
        
        :param table: Name of the table.
        :param columns: Tuple of column names.
        :param values: Tuple of values corresponding to columns.
        :return: True if successful, False otherwise.
        """
        columns_str = ", ".join(columns)
        placeholders = ", ".join(["?"] * len(values))
        query = f'''
        INSERT INTO {table}
        ({columns_str}) VALUES ({placeholders})
        '''
        return self._execute_query(query, values)

    def _remove(
        self,
        table:str,
        condition_column:str,
        condition_value:str
        ) -> bool:
        """
        Remove a record from the specified table based on a condition.
        
        :param table: Name of the table.
        :param condition_column: Column name for the condition.
        :param condition_value: Value for the condition.
        :return: True if successful, False otherwise.
        """
        query = f'''
        DELETE FROM {table}
        WHERE {condition_column} = ?
        '''
        return self._execute_query(query, (condition_value,))

    def _update(
        self,
        table_name:str,
        column:str,
        condition_column:str,
        values:tuple,
        ) -> bool:
        """
        Generic method to update a specific column value in a table based on a condition.

        :param table_name: Name of the table to update.
        :param column: Name of the column to update.
        :param condition_column: Name of the column used in the WHERE condition.
        :param values: A tuple containing the new value for the column and the value for the condition column.
                       The first value in the tuple is the new value for the column, 
                       and the second value is the value for the condition column.
        :return: True if the update was successful, False otherwise.
        """
        query = f'''
        UPDATE {table_name}
        SET {column} = ?
        WHERE {condition_column} = ?
        '''
        return self._execute_query(query, values)

    def _clean(
        self,
        table_name:str
        ) -> bool:
        """
        Remove all entries from the specified table.

        :param table_name: Name of the table to clean.
        :return: True if the cleanup was successful, False otherwise.
        """
        query = f'''
        DELETE FROM {table_name}
        '''
        return self._execute_query(query, ())

    def _get(
        self,
        table_name:str,
        column_name:str,
        condition:str,
        condition_params:tuple
        ):
        """
        Generic method to retrieve a specific column value based on a condition.

        :param table_name: Name of the table to query.
        :param column_name: Name of the column to retrieve.
        :param condition: SQL condition for the query.
        :param condition_params: Parameters for the SQL condition.
        :return: The retrieved value if found, None otherwise.
        """
        query = f'''
        SELECT {column_name} FROM {table_name}
        WHERE {condition} = ?
        '''
        self._execute_query(query, condition_params)
        result = self.cursor.fetchone()
        return result[0] if result else None

    # HACK : add a proper log function
    def _list_all_entries(
        self,
        table_name:str,
        column_name:str,
        condition:str="",
        condition_params:tuple=()
        ) -> list:
        """
        Retrieve all entries from the specified table with an optional condition.

        :param table_name: Name of the table.
        :param column_name: Name of the column to retrieve.
        :param condition: Optional SQL condition for the query.
        :param condition_params: Parameters for the SQL condition.
        :return: List of entries from the specified column.
        """
        try:
            query = f"SELECT {column_name} FROM {table_name}"
            if condition:
                query += f" WHERE {condition}"
            self.cursor.execute(query, condition_params)
            entries = self.cursor.fetchall()
            return [entry[0] for entry in entries]
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []

    # --------------------------------------------------------------------------
    # Wrapper methods

    def guild_insert(self, guild_id:str) -> bool:
        """
        Insert a new guild into the Guilds table.

        :param guild_id: The unique ID of the guild.
        :return: True if the insertion was successful, False otherwise.
        """
        return self._insert(
            "Guilds",
            ("guild_id",),
            (guild_id,)
        )

    def guild_remove(self, guild_id:str) -> bool:
        """
        Remove a guild from the Guilds table based on its ID.

        :param guild_id: The unique ID of the guild.
        :return: True if the removal was successful, False otherwise.
        """
        return self._remove(
            "Guilds",
            "guild_id",
            guild_id
        )

    def parent_chan_insert(self, guild_id:str, parent_chan_id:str) -> bool:
        """
        Insert a new parent channel into the ParentChannels table.

        :param guild_id: The unique ID of the guild.
        :param parent_chan_id: The unique ID of the parent channel.
        :return: True if the insertion was successful, False otherwise.
        """
        return self._insert(
            "ParentChannels",
            ("guild_id", "parent_channel_id"),
            (guild_id, parent_chan_id)
        )

    def parent_chan_remove(self, chan_id:str) -> bool:
        """
        Remove a parent channel from the ParentChannels table based on its ID.

        :param chan_id: The unique ID of the parent channel.
        :return: True if the removal was successful, False otherwise.
        """
        return self._remove(
            "ParentChannels",
            "parent_channel_id",
            chan_id
        )

    def temporary_chan_insert(self, parent_chan_id:str, chan_id:str) -> bool:
        """
        Insert a new temporary channel into the TemporaryChannels table.

        :param chan_id: The unique ID of the temporary channel.
        :return: True if the removal was successful, False otherwise.
        """
        return self._insert(
            "TemporaryChannels",
            ("parent_channel_id", "temporary_channel_id"),
            (parent_chan_id, chan_id,)
        )

    def temporary_chan_remove(self, chan_id:str) -> bool:
        """
        Remove a temporary channel from the TemporaryChannels table based on its ID.

        :param chan_id: The unique ID of the temporary channel.
        :return: True if the removal was successful, False otherwise.
        """
        return self._remove(
            "TemporaryChannels",
            "temporary_channel_id",
            chan_id
        )

    def temporary_channel_clean(self) -> bool:
        """
        Remove all entries from the TemporaryChannels table.

        :return: True if the cleanup was successful, False otherwise.
        """
        return self._clean("TemporaryChannels")

    def template_update(self, name_template:str, parent_channel_id:str) -> bool:
        """
        Update the name_template value for a specific parent_channel_id in the ParentChannels table.

        :param name_template: The new template value to set.
        :param parent_channel_id: The ID of the parent channel for which the template should be updated.
        :return: True if the update was successful, False otherwise.
        """
        return self._update(
            "ParentChannels",
            "name_template",
            "parent_channel_id",
            (name_template, parent_channel_id,)
        )

    def get_all_guilds(self) -> list:
        """
        Wrapper method to retrieve all guilds from the Guilds table.

        :return: List of guild IDs.
        """
        return self._list_all_entries("Guilds", "guild_id")

    def get_all_parent_channels(self) -> list:
        """
        Wrapper method to retrieve all parent channels from the ParentChannels table.

        :return: List of temporary channels IDs.
        """
        return self._list_all_entries("ParentChannels", "parent_channel_id")

    def get_all_temporary_channels(self) -> list:
        """
        Wrapper method to retrieve all temporary channels from the TemporaryChannels table.

        :return: List of temporary channels IDs.
        """
        return self._list_all_entries("TemporaryChannels", "temporary_channel_id")

    def get_parent_channels_for_guild(self, guild_id:str) -> list:
        """
        Wrapper method to retrieve all parent channels for a given guild.

        :param guild_id: The ID of the guild.
        :return: List of parent channel IDs associated with the guild.
        """
        return self._list_all_entries(
            "ParentChannels",
            "parent_channel_id",
            "guild_id = ?",
            (guild_id,)
        )

    def get_child_channels_for_parent(self, parent_channel_id:str) -> list:
        """
        Wrapper method to retrieve all child channels for a given parent channel.

        :param parent_channel_id: The ID of the parent channel.
        :return: List of child channel IDs associated with the parent channel in the guild.
        """
        return self._list_all_entries(
            "TemporaryChannels",
            "temporary_channel_id",
            "parent_channel_id = ?",
            (parent_channel_id,)
        )

    def get_name_template(self, parent_channel_id:str):
        """
        Retrieve the name_template value for a specific parent_channel_id from the ParentChannels table.

        :param parent_channel_id: The ID of the parent channel.
        :return: The name_template value if found, None otherwise.
        """
        return self._get(
            "ParentChannels",
            "name_template",
            "parent_channel_id",
            (parent_channel_id,)
        )
