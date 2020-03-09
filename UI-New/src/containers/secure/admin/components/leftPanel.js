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
    textAlign: "center",
    borderBottom: '2px solid #fff',

  },
  round: {
    margin: '20px 0',
    fontSize: "22px",
    textAlign: "center",
    padding: "20px 0",
    color: "white"
  },
  lastMoves:{
  padding: "20 0",
  textAlign: "center",
  background: "white",
  color: "black",
  fontSize: "23px"
},
  players: {
    margin: "40px 0"
  },
  playerStatus: {
    textAlign: "center",
    background: "cornflowerblue",
    fontSize: "30px",
    padding: "20px 0"
  },
  lastMovesList: {
    fontSize: '20px',
    color: "white",
    padding: "0 20px",
    textAlign: "center",
    margin: "20px 0",
    height: "120px",
    overflow: "auto"
  },
  score: {
    fontSize: '22px',
    borderTop: '2px solid #fff',
    margin: '20px 0',
    padding: '20px 0'
  },
  top: {
    fontSize: '22px',
    margin: '0 0 20px',

  },
  button: {
    textAlign: 'center',
  },
  buttonSize: {
    fontSize: '30px'
  }

};

// TODO: Implement select design
class LeftPanel extends React.Component {
  state = {
    ghostList: [],
    round: -1,
    epoch: -1,
    ghostbuster: 0,
    ghost: 0,
    resources: [[],[],[],[],[],[]]
  };

  componentDidMount() {
    var that= this;
    var round = firebase.database().ref('ghostbuster/round');
      round.on('value', function(snapshot) {
        that.updateRound(snapshot.val())
      });

      var ghost_last = firebase.database().ref('ghostbuster/ghostLastMove');
      ghost_last.on('value', function(snapshot) {
        that.updateghostlist(snapshot.val())
      });
      var epoch = firebase.database().ref('ghostbuster/epoch');
        epoch.on('value', function(snapshot) {
          that.setState({
            epoch: snapshot.val()
          })
        });
      var ghost_win = firebase.database().ref('ghostbuster/ghost_win');
        ghost_win.on('value', function(snapshot) {
          alert("Ghost win");
          that.setState({
            ghost: snapshot.val()
          })
        });

        var busters_win = firebase.database().ref('ghostbuster/busters_win');
          busters_win.on('value', function(snapshot) {
            alert("Ghost busters win");
            that.setState({
              ghostbuster: snapshot.val()
            })
          });
          var resources = firebase.database().ref('ghostbuster/resources');
            resources.on('value', function(snapshot) {
              that.setState({
                resources: snapshot.val()
              })
            });



  }

  updateghostlist = (value) => {
    var l = this.state.ghostList;
    l.push(value);
    this.setState({
      ghostList: l
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
    }, {
      name: 'E',
      color: 'pink'
    }]
    return (
      <div className="left-panel">
        <div className={classes.header}>
          Ghost busters
          <div className={classes.score}>
            Epoch : {this.state.epoch}/1000
          </div>

          <div className={classes.top}>
            <div className={classes.top}>
              Ghost Wins: {this.state.ghost}
            </div>
            <div className={classes.top}>
              Ghost Buster Wins: {this.state.ghostbuster}
            </div>
          </div>
        </div>
        <div className={classes.round}>
          Round : {this.state.round}/24
        </div>
        <div className={classes.lastMoves}>
          Ghost Last Moves
        </div>
        <div className={classes.lastMovesList}>
        {this.state.ghostList.map((list) => (
          <div>
            {list} <br/>
          </div>
        ))}
        </div>


        <div className={classes.players}>
          <div className={classes.lastMoves}>Players Status</div>
          {players.map((player, i) => (
            <Player player={player} resources = {this.state.resources[i]} />
          ))}
        </div>
        <div className={classes.button}>
        <button className={classes.buttonSize} onClick={this.props.startTrain}>
          Train
        </button>

        <button className={classes.buttonSize} onClick={this.props.startTest}>
          Test
        </button>
        </div>

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
