const messageTableName = 'message';
const translationTableName = 'translation';

export default {
  message: {
    name: messageTableName,
    columns: {
      id: `\`${messageTableName}\`.\`id\``,
      key: `\`${messageTableName}\`.\`key\``,
      createdAt: `\`${messageTableName}\`.\`createdAt\``,
    },
  },
  translation: {
    name: translationTableName,
    columns: {
      id: `\`${translationTableName}\`.\`id\``,
      body: `\`${translationTableName}\`.\`body\``,
      lcid: `\`${translationTableName}\`.\`lcid\``,
      messageId: `\`${translationTableName}\`.\`messageId\``,
      createdAt: `\`${translationTableName}\`.\`createdAt\``,
      updatedAt: `\`${translationTableName}\`.\`updatedAt\``,
    },
  },
};
