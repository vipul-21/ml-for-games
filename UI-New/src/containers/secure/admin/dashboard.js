import React from 'react';
import { connect } from 'react-redux';
import withStyles from "@material-ui/core/styles/withStyles";
import InputLabel from "@material-ui/core/InputLabel";
import firebase from "firebase/app";
import "firebase/database";
import {
  FirebaseDatabaseProvider,
  FirebaseDatabaseNode
} from "@react-firebase/database";

import LightTheme from '../../../components/background/light'
// import CardAvatar from '../../components/Card/CardAvatar'
import Card from '../../../components/Card/Card'
// import CardBody from '../../components/Card/CardBody'
// import ButtonProvider from '../../components/common/button'
// import ImageProvider from '../../components/ImageProvider'
import Loader from '../../../components/common/loader'
import LeftPanel from './components/leftPanel'
import RightPanel from './components/rightPanel'

// import first from '../../assets/first.jpg';
// import second from '../../assets/second.jpg';
// import logo from '../../assets/logo.png';

import './dashboard.css';

const firebaseConfig = {
  apiKey: 'AIzaSyC0F_r19UKFUmQRUesHSVq3qpBgXdGB0OE',
  authDomain: 'voteusc.firebaseapp.com',
  databaseURL: 'https://voteusc.firebaseio.com',
  projectId: 'voteusc',
  storageBucket: 'voteusc.appspot.com',
  messagingSenderId: '379614556768'
};


const styles = {
  cardCategoryWhite: {
    color: "rgba(255,255,255,.62)",
    margin: "0",
    fontSize: "14px",
    marginTop: "0",
    marginBottom: "0"
  },
  cardTitle: {
    marginTop: "0px",
    minHeight: "auto",
    fontWeight: "600",
    fontSize: '20px',
    marginBottom: "3px",
    textDecoration: "none",
    display: 'flex',
  },
  team: {
    display: 'flex',
    alignItems: 'center'
  },
  candidateContainer: {
    display: 'flex',
    padding: '0 20px',
  },
  candidate: {
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'center',
  },
  candidateName: {
    fontSize: '12px',
    fontWeight: '300',
    padding: '5px 0',
  }
};

// TODO: Implement select design
class Dashboard extends React.Component {
  state = {
    parties: this.props.parties,
    round: -1
  };

  componentDidMount() {
    this.props.getData();
    // this.props.getScores();
    // this.props.getFlow();
    // this.props.get();

  }

  static getDerivedStateFromProps(props, state) {
    // ...
    return {
        parties: props.parties
      };

  }
  render() {
    const {classes, parties} = this.props;
    return (
        <LightTheme className="grey" grey>
          <div className="admin-container">
            <LeftPanel round ={this.state.round}/>
            <RightPanel />

          </div>
        </LightTheme>
      )
    }
}

const mapStateToProps = state => {
  return { result: state.main.result,
    maliciousData: state.main.maliciousData,
  scores: state.main.scores,
 flow: state.main.flow
};
};

const mapDispatchToProps = (dispatch) => {
  return {
    getAllParties: () => {
      dispatch({ type: 'GET_ALL_PARTIES_INIT' })
    },
    getData: () => {
      dispatch({ type: 'GET_DATA_INIT' })
    },
    voteForParty:(partyId) => {
      dispatch({ type: 'VOTE_INIT', partyId })
    },
    getAddress:() => {
      dispatch({ type: 'GET_ADDRESS_INIT' })
    },
    getScores:() => {
      dispatch({ type: 'GET_SCORES_INIT' })
    },
    getFlow:() => {
      dispatch({ type: 'GET_FLOW_INIT' })
    },
    get:() => {
      dispatch({ type: 'GET_ZETA_INIT' })
    }

  }
}

export default connect(mapStateToProps, mapDispatchToProps)(withStyles(styles)(Dashboard));
// export default withStyles(styles)(Vote);
