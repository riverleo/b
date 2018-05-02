from contrib import db, dumps, split
from orator.query.join_clause import JoinClause


def handler(event, context):
    sql = db.table('work')
    query_params = event.get('queryStringParameters') or {}

    authors = split(query_params.get('authors'))
    categories = split(query_params.get('categories'))

    if authors:
        sql = (
            sql.join('workRole', 'work.id', '=', 'workRole.workId')
            .where('workRole.type', 'author')
            .where_in('workRole.userId', authors)
        )

    if categories:
        sql = (
            sql.join(
                JoinClause('categoryMap')
                .on('work.id', '=', 'categoryMap.categorizableId')
                .where('categoryMap.categorizableType', '=', 'work')
            )
            .join('category', 'category.id', '=', 'categoryMap.categoryId')
            .where_in('category.key', categories)
        )

    return {
        'body': dumps({'data': sql.get()}),
        'headers': {'Access-Control-Allow-Origin': '*'},
        'statusCode': 200,
    }
