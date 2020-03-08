import axios from 'axios';

const baseUrl = 'https://voteusc.herokuapp.com';
var db = null;

const formatData = (response) => {
    if(response.status === 200) {
      return {
        success: true,
        result: response.data.result
      }
    }
    else if(response.status === 202) {
      return {
        success: true,
        result: response.data.response
      }
    } else {
      return {
        success: false
      }
    }
}
export function getData() {

  // const response = axios.get(`${baseUrl}/party/all`, {
  //   headers: {
  //     "X-APP-TOKEN": "tcic"
  //   }
  // }).then(res => formatData(res));

  const response = db.collection("zeta/").doc("1").get().then((doc) =>
    // querySnapshot.forEach((doc) =>
        doc.data()
  // )
);
console.log(response);
  return response;
}

export function getScores() {
  const response = db.collection("zeta/").doc("scores").get().then((doc) =>
        doc.data());
  return response;
}


export function getFlow() {

  const response = db.collection("zeta/").doc("flow").get().then((doc) =>
        doc.data()
);
console.log(response);
  return response;
}


export function getZetaData(address) {
  console.log('here', address);
  // var ref = firebase.database().ref("zeta/1/nodes");
  // const response = ref.once("value")
  //   .then(function(snapshot) {
  //     // var key = snapshot.key; // "ada"
  //     // var childKey = snapshot.child("name/last").key; // "last"
  //     console.log(snapshot.val());
  //     formatData(snapshot)
  //   });
  //
  // // const response = axios.get(`${baseUrl}/party/all`, {
  // //   headers: {
  // //     "X-APP-TOKEN": "tcic"
  // //   }
  // // }).then(res => formatData(res));
  // return response;
  const response = axios.get(`https://zetascore.herokuapp.com/money/0x821aEa9a577a9b44299B9c15c88cf3087F3b5544`, {headers: {
        "X-APP-TOKEN": "tcic"
      }}
).then(res => res);
  return response;

}

export function startProcess() {
  const response = axios.get(`http://localhost:8000/start`).then(res =>
    formatData(res));
  return response;
}


export function postData(partyId) {
  const response = axios.post(`${baseUrl}/party/${partyId}/vote`,{ "id": partyId }, {
    headers: {
      "X-APP-TOKEN": "tcic"
    }
  }).then(res => formatData(res));
  return response;
}
