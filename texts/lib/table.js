const textTableName = 'text';
const translationTableName = 'translation';

export default {
  name: textTableName,
  columns: {
    id: `${textTableName}.id`,
    key: `${textTableName}.key`,
    createdAt: `${textTableName}.createdAt`,
  },
};

export const translation = {
  name: translationTableName,
  columns: {
    id: `${translationTableName}.id`,
    body: `${translationTableName}.body`,
    locale: `${translationTableName}.locale`,
    textId: `${translationTableName}.textId`,
    createdAt: `${translationTableName}.createdAt`,
    updatedAt: `${translationTableName}.updatedAt`,
  },
};
