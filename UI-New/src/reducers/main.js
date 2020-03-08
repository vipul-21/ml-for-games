const inital = {
  parties: [],
  feedbackUrl: '',
  feedbackMessage: ''
}

const main = (state = inital, action) => {
  switch (action.type) {
    case 'INITIAL_STATE': {
      return action.state;
    }
    case 'GET_ALL_PARTIES_DONE': {

      return { ...state, parties: action.result };
    }
    case 'GET_ALL_PARTIES_INIT': {
      return state;
    }
    case 'GET_ALL_PARTIES_FAIL': {
      return action.state;
    }
    case 'VOTE_DONE': {
      return { ...state, feedbackUrl: action.result.url, feedbackMessage: action.result.message };
    }
    case "GET_DATA_DONE": {
      return {...state, result: action.result}
    }
    case "GET_ADDRESS_DONE": {
      return {...state, maliciousData: action.result}
    }
    case "GET_SCORES_DONE": {
      return {...state, scores: action.result}
    }
    case "GET_FLOW_DONE": {
      return {...state, flow: action.result}
    }
    case "GET_MALICIOUS_DONE": {
      return {...state, malicious: action.result}
    }
    case "GET_ZETA_DONE": {
      return {...state, zetaData: action.result}
    }

    default: return state;
  }
};

export default main;
