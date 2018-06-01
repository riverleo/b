const _ = require('lodash');
const mock = require('./mock');
const parseFormData = require('./formData');

describe('formData.js', () => {
  it('폼 이름이 올바른 경우', () => {
    const parsed = parseFormData(mock.event);

    expect(parsed).toHaveProperty('user1');
    expect(parsed).toHaveProperty('user1.type', 'file');
    expect(parsed).toHaveProperty('user1.filename', 'user1.json');
    expect(parsed).toHaveProperty('user1.content');
    expect(parsed).toHaveProperty('user1.contentType', 'application/json');
    expect(parsed).toHaveProperty('user2');
    expect(parsed).toHaveProperty('user2.type', 'file');
    expect(parsed).toHaveProperty('user2.filename', 'user2.json');
    expect(parsed).toHaveProperty('user2.content');
    expect(parsed).toHaveProperty('user2.contentType', 'application/json');
    expect(parsed).toHaveProperty('lcid');
    expect(parsed).toHaveProperty('lcid.content', 'en-US');
  });

  it('폼 이름이 올바르지 않은 경우', () => {
    const parsed = parseFormData(mock.eventWithoutInputName);
    const keys = _.keys(parsed);

    expect(parsed).toHaveProperty(`${keys[0]}.type`, 'file');
    expect(parsed).toHaveProperty(`${keys[0]}.filename`, 'file.json');
    expect(parsed).toHaveProperty(`${keys[0]}.content`);
    expect(parsed).toHaveProperty(`${keys[0]}.contentType`, 'application/json');
    expect(parsed).toHaveProperty(`${keys[1]}.type`, 'file');
    expect(parsed).toHaveProperty(`${keys[1]}.filename`, 'image.jpg');
    expect(parsed).toHaveProperty(`${keys[1]}.content`);
    expect(parsed).toHaveProperty(`${keys[1]}.contentType`, 'image/jpeg');
  });

  it('이미지 파일이 올라온 경우', () => {
    const parsed = parseFormData(mock.eventWithImage);

    expect(parsed).toHaveProperty('json');
    expect(parsed).toHaveProperty('json.type', 'file');
    expect(parsed).toHaveProperty('json.filename', 'file.json');
    expect(parsed).toHaveProperty('json.content');
    expect(parsed).toHaveProperty('json.contentType', 'application/json');
    expect(parsed).toHaveProperty('cloud');
    expect(parsed).toHaveProperty('cloud.type', 'file');
    expect(parsed).toHaveProperty('cloud.filename', 'image.jpg');
    expect(parsed).toHaveProperty('cloud.content');
    expect(parsed).toHaveProperty('cloud.contentType', 'image/jpeg');
  });
});
