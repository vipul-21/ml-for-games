const TOKEN_KEY = 'vote_on_chain';
const TOKEN_STATUS = '0'
class TokenStorage {
  static token;

  static setToken(token: string) {
    TokenStorage.token = token;
    window.localStorage.setItem(TOKEN_KEY, token);
  }

  static getToken() {
    if (TokenStorage.token === undefined) {
      TokenStorage.token = window.localStorage.getItem(TOKEN_KEY);
    }
    return TokenStorage.token;
  }

  static clear() {
    TokenStorage.token = null;
    Object.keys(window.localStorage).forEach(key => window.localStorage.removeItem(key));
  }
  static setStatus(token: string) {
    TokenStorage.status = token;
    window.localStorage.setItem(TOKEN_STATUS, token);
  }

  static getStatus() {
    if (TokenStorage.status === undefined) {
      TokenStorage.status = window.localStorage.getItem(TOKEN_STATUS);
    }
    return TokenStorage.status;
  }

  static clear() {
    TokenStorage.status = null;
    Object.keys(window.localStorage).forEach(key => window.localStorage.removeItem(key));
  }
}

export default TokenStorage;
