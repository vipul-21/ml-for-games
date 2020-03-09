import React from 'react';
import {Link} from 'react-router-dom'
import { connect } from 'react-redux';
import withStyles from "@material-ui/core/styles/withStyles";
import InputLabel from "@material-ui/core/InputLabel";

// import CardAvatar from '../../components/Card/CardAvatar'
import Card from '../../../../components/Card/Card'
// import CardBody from '../../components/Card/CardBody'
// import ButtonProvider from '../../components/common/button'
import ImageProvider from '../../../../components/ImageProvider'
import Loader from '../../../../components/common/loader'
import Player from '../../Player';

// import first from '../../assets/first.jpg';
// import second from '../../assets/second.jpg';
import logo from '../../../../assets/logo-white.png';
import dashboard from '../../../../assets/dashboard.svg';
import dashboard1 from '../../../../assets/dashboard-1.svg';
import tree from '../../../../assets/tree.svg';
import search from '../../../../assets/search.svg';

import './leftPanel.css';

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
  },
  header: {
    color: "#fff",
    fontSize: "48px",
    textAlign: "center"
  },
  round: {
    fontSize: "35px",
    textAlign: "center",
    padding: "20px 0",
    background: "white"
  },
  lastMoves:{
  padding: "40px 0",
  textAlign: "center",
  background: "yellow",
  fontSize: "20px"
},
  players: {
    margin: "40px 0"
  },
  playerStatus: {
    textAlign: "center",
background: "cornflowerblue",
fontSize: "30px",
padding: "20px 0"
  }
};

// TODO: Implement select design
class LeftPanel extends React.Component {
  state = {
    parties: this.props.parties,
    round: -1
  };

  componentDidMount() {
    var that= this;
    var round = firebase.database().ref('ghostbuster/round');
      round.on('value', function(snapshot) {
        that.updateRound(snapshot.val())
      });
  }
  updateRound = (value) => {
    this.setState({
      round: value
    })
  }


  render() {
    const {classes, parties,round} = this.props;
    const players = [{
      name: "A",
      color: "red"
    }, {
      name: "B",
      color: "yellow"
    }, {
      name: "C",
      color: "blue"
    }, {
      name: "D",
      color: "green"
    }]
    return (
      <div className="left-panel">
        <div className={classes.header}>
          GHOST BUSTERS
        </div>
        <div className={classes.round}>
          Round : {this.state.round}/24
        </div>
        <div className={classes.lastMoves}>
          Ghost Last Moves
        </div>


        <div className={classes.players}>
          <div className={classes.playerStatus}>Players Status</div>
          {players.map((player) => (
            <Player player={player} />
          ))}
        </div>
        <button onClick={this.props.startTrain}>
          Train
        </button>

        <button onClick={this.props.startTest}>
          Test
        </button>

      </div>
    )

    }
}

const mapStateToProps = state => {
  return { parties: state.main.parties };
};

const mapDispatchToProps = (dispatch) => {
  return {
    getAllParties: () => {
      dispatch({ type: 'GET_ALL_PARTIES_INIT' })
    },
    voteForParty:(partyId) => {
      dispatch({ type: 'VOTE_INIT', partyId })
    },
    startTrain:() => {
      dispatch({ type: 'TRAIN_INIT' })
    },
    startTest:() => {
      dispatch({ type: 'TEST_INIT' })
    }


  }
}

export default connect(mapStateToProps, mapDispatchToProps)(withStyles(styles)(LeftPanel));
// export default withStyles(styles)(Vote);
