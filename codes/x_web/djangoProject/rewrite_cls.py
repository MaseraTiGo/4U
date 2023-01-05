# -*- coding: utf-8 -*-
# @File    : rewrite_cls
# @Project : ifw_ng_mw
# @Time    : 2022/12/6 15:56
# once, I want 2 leave my name 2 the history
# sadly, I find that my hair gets pale
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""

from django.db.migrations.migration import Migration
from django.db.transaction import atomic


class MyFuckingMigration(Migration):
    def apply(self, project_state, schema_editor, collect_sql=False):
        """
        Take a project_state representing all migrations prior to this one
        and a schema_editor for a live database and apply the migration
        in a forwards order.

        Return the resulting project state for efficient reuse by following
        Migrations.
        """
        for operation in self.operations:
            # If this operation cannot be represented as SQL, place a comment
            # there instead
            try:
                if collect_sql:
                    schema_editor.collected_sql.append("--")
                    if not operation.reduces_to_sql:
                        schema_editor.collected_sql.append(
                            "-- MIGRATION NOW PERFORMS OPERATION THAT CANNOT BE WRITTEN AS SQL:"
                        )
                    schema_editor.collected_sql.append(
                        "-- %s" % operation.describe())
                    schema_editor.collected_sql.append("--")
                    if not operation.reduces_to_sql:
                        continue
                # Save the state before the operation has run
                old_state = project_state.clone()
                operation.state_forwards(self.app_label, project_state)
                # Run the operation
                atomic_operation = operation.atomic or (
                            self.atomic and operation.atomic is not False)
                if not schema_editor.atomic_migration and atomic_operation:
                    # Force a transaction on a non-transactional-DDL backend or an
                    # atomic operation inside a non-atomic migration.
                    with atomic(schema_editor.connection.alias):
                        operation.database_forwards(self.app_label,
                                                    schema_editor, old_state,
                                                    project_state)
                else:
                    # Normal behaviour
                    operation.database_forwards(self.app_label, schema_editor,
                                                old_state, project_state)
            except Exception as e:
                print(f"dong ---------------> apply failed, but will be ignored"
                      f": {e}")
                pass
        return project_state
