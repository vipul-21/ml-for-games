import { takeEvery, put, call, takeLatest } from 'redux-saga/effects';
import { push, goBack } from 'react-router-redux';
import TokenStorage from '../services/TokenStorage';
import { getUser, getAllParties, voteForParty, getAddress, getData, getScores,
   getFlow, getZetaData,startProcess } from '../api/apiClient';


function* getAllPartiesInit() {
  try {
    const data = yield call(getAllParties);
    if (data.success) {
      yield put({ type: 'GET_ALL_PARTIES_DONE', result: data.result })
    }
  } catch (e) {
    yield put({ type: 'GET_ALL_PARTIES_FAIL', message: e.message });
  }
}

function* postVoteInit(action) {
  try {
    const data = yield call(voteForParty, action.partyId);
    if (data.success) {
      yield put({ type: 'VOTE_DONE', result: data.result })
      yield put(push('/feedback'));

    }
  } catch (e) {
    // yield put({ type: 'GET_USER_FAILED', message: e.message });
  }
}

function* getAddressInit(action) {
  try {
    const data = yield call(getAddress);
    console.log(data)
    if (data.success) {

      yield put({ type: 'GET_ADDRESS_DONE', result: data.result })
      // yield put(push('/feedback'));

    }
  } catch (e) {
    // yield put({ type: 'GET_USER_FAILED', message: e.message });
  }
}

function* getDataInit(action) {
  try {
    // console.log('ho');
    const data = yield call(startProcess);
    console.log(data)

    yield put({ type: 'GET_DATA_DONE'})
      // yield put(push('/feedback'));


  } catch (e) {
    // yield put({ type: 'GET_USER_FAILED', message: e.message });
  }
}

function* signinAdminInit(action) {
  try {
      yield put(push('/admin'));
  } catch (e) {
    // yield put({ type: 'GET_USER_FAILED', message: e.message });
  }
}

function* signinPulicInit(action) {
  try {
      TokenStorage.setToken(action.email)
      yield put(push('/vote'));
  } catch (e) {
    // yield put({ type: 'GET_USER_FAILED', message: e.message });
  }
}
function* getZetaInit(action) {
  try {
    const data = yield call(getZetaData);
    console.log(data)
    // if (data.success) {

      yield put({ type: 'GET_ZETA_DONE', result: data.data })
      // yield put(push('/feedback'));

    // }
  } catch (e) {
    // yield put({ type: 'GET_USER_FAILED', message: e.message });
  }
}

function* getFlowInit(action) {
  try {
    const data = yield call(getFlow);
    // console.log(data)
    // if (data.success) {

      yield put({ type: 'GET_FLOW_DONE', result: data })
      // yield put(push('/feedback'));

    // }
  } catch (e) {
    // yield put({ type: 'GET_USER_FAILED', message: e.message });
  }
}

function* getMaliciousInit(action) {
  try {
    console.log(action.address);
    const web3 = new Web3(Web3.givenProvider || 'ws://localhost:8546', null, {});
    console.log(web3);


    var ZetaContract = web3.eth.Contract([
{
 "constant": false,
 "inputs": [
   {
     "name": "_address",
     "type": "address"
   },
   {
     "name": "_score",
     "type": "string"
   }
 ],
 "name": "Upload",
 "outputs": [],
 "payable": false,
 "stateMutability": "nonpayable",
 "type": "function"
},
{
 "inputs": [],
 "payable": false,
 "stateMutability": "nonpayable",
 "type": "constructor"
},
{
 "constant": true,
 "inputs": [],
 "name": "owner",
 "outputs": [
   {
     "name": "",
     "type": "address"
   }
 ],
 "payable": false,
 "stateMutability": "view",
 "type": "function"
},
{
 "constant": true,
 "inputs": [
   {
     "name": "_address",
     "type": "address"
   }
 ],
 "name": "retrieve",
 "outputs": [
   {
     "name": "x",
     "type": "bytes"
   }
 ],
 "payable": false,
 "stateMutability": "view",
 "type": "function"
},
{
 "constant": true,
 "inputs": [
   {
     "name": "",
     "type": "address"
   },
   {
     "name": "",
     "type": "uint256"
   }
 ],
 "name": "score",
 "outputs": [
   {
     "name": "",
     "type": "string"
   }
 ],
 "payable": false,
 "stateMutability": "view",
 "type": "function"
}
]);
  ZetaContract.address = "0x39ee1385ae32550e2163f21c53a5714b86879ffe";
 //    var Zeta = ZetaContract.at('0x39ee1385ae32550e2163f21c53a5714b86879ffe');
 // console.log(Zeta);
//  const data  = yield ZetaContract.methods.retrieve(action.address).call()
//  .then(res => {
//       var str = '';
//       for (var i = 0; i < res.length; i += 2) {
//       var v = parseInt(res.substr(i, 2), 16);
//       if (v) str += String.fromCharCode(v);
//       }
//
//       let params = [];
//       let result = "";
//       for (var i=0; i<= str.length; i++){
//       if(str.charCodeAt(i) > 31){
//       result = result + str[i];
//       }
//       else{
//       params.push(result);
//       result = "";
//       }
//       }
//       params.pop();
//
//       return params
//
// } );

const data  = yield ZetaContract.methods.retrieve(action.address).call().then(res => {
     var str = '';
     for (var i = 0; i < res.length; i += 2) {
     var v = parseInt(res.substr(i, 2), 16);
     if (v) str += String.fromCharCode(v);
     }
     console.log('response',res);

     let params = [];
     let result = "";
     for (var i=0; i<= str.length; i++){
     if(str.charCodeAt(i) > 31){
     result = result + str[i];
     }
     else{
     params.push(result);
     result = "";
     }
     }
     params.pop();

     return params

})

// const test = ZetaContract.methods.retrieve(action.address).on().then(res => {
// .on('transactionHash', (hash) => {
//   console.log("SDFASDFS",hash)
// });

console.log('Data:', data);
let mani_data = data.map(val => { return {value:val, address: action.address}})
yield put({ type: 'GET_MALICIOUS_DONE', result: mani_data })


//
//     // $("#updatescore").click(function() {
//     //     Zeta.Upload.sendTransaction( $("#addr").val(), $("#zet").val(), {
//     //      from:web3.eth.accounts[0],
//     //      gas:4000000}, (err, res) => {
//     //         if (err) {
//     //             console.log("error in Upload!")
//     //         }
//     //     });
//     //  });
//
//   // $("#showhistory").click(function() {
//   console.log(Zeta.retrieve(action.address));
//    Zeta.retrieve(action.address).then(res => {
//      if (res) {
//
//         var str = '';
// for (var i = 0; i < res.length; i += 2) {
//    var v = parseInt(res.substr(i, 2), 16);
//    if (v) str += String.fromCharCode(v);
// }
//
//   params = [];
// result = "";
// for (var i=0; i<= str.length; i++){
//   if(str.charCodeAt(i) > 31){
//     result = result + str[i];
//   }
//   else{
//     params.push(result);
//     result = "";
//   }
// }
// params.pop();
//     console.log(params)
//   }});




      // yield put(push('/feedback'));

    // }
  } catch (e) {
    console.log(e);
  }
}
function* getScoresInit(action) {
  try {
    const data = yield call(getScores);
    // console.log(data)
    // if (data.success) {

      yield put({ type: 'GET_SCORES_DONE', result: data })
      // yield put(push('/feedback'));

    // }
  } catch (e) {
    // yield put({ type: 'GET_USER_FAILED', message: e.message });
  }
}

function* saga() {
  yield takeEvery('GET_ALL_PARTIES_INIT', getAllPartiesInit);
  yield takeEvery('VOTE_INIT', postVoteInit);
  yield takeEvery('SIGNIN_ADMIN_INIT', signinAdminInit);
  yield takeLatest('GET_DATA_INIT', getDataInit);
  yield takeEvery('GET_ZETA_INIT', getZetaInit);
  yield takeEvery('GET_SCORES_INIT', getScoresInit);
  yield takeEvery('GET_FLOW_INIT', getFlowInit);
  yield takeLatest('GET_MALICIOUS_INIT', getMaliciousInit);
  yield takeEvery('GET_ADDRESS_INIT', getAddressInit);
  yield takeEvery('SIGNIN_PUBLIC_INIT', signinPulicInit);
}

export default saga;
