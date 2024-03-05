from sql_to_ast.select_ast_builder import SelectAstBuilder

from ast_to_ef.adapter import select_clause, from_clause, where_clause


def build_ef(sql: str):
    ast = SelectAstBuilder.build(sql)

    return f"{from_clause.build_from(ast.from_clause)}\n{where_clause.build_where(ast.where_clause)}\n{select_clause.build_select(ast.select_clause)}"


def main():
    # sql = f"""
    # SELECT T1.fname ,  T1.lname FROM Faculty AS T1 JOIN Student AS T2 ON T1.FacID  =  T2.advisor WHERE T2.fname  =  'Linda' AND T2.lname  = 'Smith'
    # """

    # sql = f"""
    # SELECT count(*) FROM Has_allergy AS T1 JOIN Allergy_type AS T2 ON T1.allergy  =  T2.allergy WHERE T2.allergytype  =  'food'
    # """

    sql = f"""
    SELECT DISTINCT T2.Model
    FROM CAR_NAMES AS T1
    JOIN MODEL_LIST AS T2 ON T1.Model  =  T2.Model
    JOIN CAR_MAKERS AS T3 ON T2.Maker  =  T3.Id
    JOIN CARS_DATA AS T4 ON T1.MakeId  =  T4.Id
    WHERE T3.FullName  =  'General Motors' OR T4.weight  >  3500
    """

    ef = build_ef(sql)

    print(ef)


if __name__ == "__main__":
    main()
