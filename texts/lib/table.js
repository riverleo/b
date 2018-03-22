const textTableName = 'text';
const translationTableName = 'translation';

export default {
  text: {
    name: textTableName,
    columns: {
      id: `\`${textTableName}\`.\`id\``,
      key: `\`${textTableName}\`.\`key\``,
      createdAt: `\`${textTableName}\`.\`createdAt\``,
    },
  },
  translation: {
    name: translationTableName,
    columns: {
      id: `\`${translationTableName}\`.\`id\``,
      body: `\`${translationTableName}\`.\`body\``,
      lcid: `\`${translationTableName}\`.\`lcid\``,
      textId: `\`${translationTableName}\`.\`textId\``,
      createdAt: `\`${translationTableName}\`.\`createdAt\``,
      updatedAt: `\`${translationTableName}\`.\`updatedAt\``,
    },
  },
};
