// import { mount } from '@vue/test-utils';
import each from 'jest-each';
import AudioBooks from '@/components/AudioBooks.vue';

describe('value comparison', () => {
  each([
    ['Alice', 'Bob', -1],
    ['Alice', 'Alice', 0],
    ['Bob', 'Alice', 1],
    ['Alice', null, -1],
    [null, null, 0],
    [1, 2, -1],
    [1, 1, 0],
    [2, 1, 1],
    [null, 1, 1],
  ]).it("when the input is '%s' and '%s'", (lhs, rhs, expected) => {
    const cmp = AudioBooks.cmp(lhs, rhs);
    expect(cmp).toEqual(expected);
  });
});

describe('audibook comparison', () => {
  each([
    [
      { artist: 'Bob der Baumeister', disc: 1, title: 'Bob hilft dem Weihnachtsmann' },
      { artist: 'Bob der Baumeister', disc: 1, title: 'Spass im Schnee' },
      -1,
    ],
    [
      { artist: 'Bob der Baumeister', disc: 3, title: 'Bob hilft dem Weihnachtsmann' },
      { artist: 'Leo Lausemaus', disc: 1, title: 'Will nicht baden' },
      -1,
    ],
    [
      { artist: 'Bob der Baumeister', disc: null, title: 'Bob hilft dem Weihnachtsmann' },
      { artist: 'Bob der Baumeister', disc: 1, title: 'Bob hilft dem Weihnachtsmann' },
      1,
    ],
  ]).it("when the input is '%s' and '%s'", (lhs, rhs, expected) => {
    const cmp = AudioBooks.methods.cmpAudioBooks(lhs, rhs);
    expect(cmp).toEqual(expected);
  });
});
