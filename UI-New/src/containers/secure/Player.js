import React from 'react';
import {Link} from 'react-router-dom'
import { connect } from 'react-redux';
import withStyles from "@material-ui/core/styles/withStyles";
import InputLabel from "@material-ui/core/InputLabel";

import './Player.css';
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
  name: {
    fontSize: "40px",
    padding: "20px",
    color: "white",
    alignItems:"center",
    display: 'flex',
    justifyContent: "center"
  }
};

// TODO: Implement select design
class Player extends React.Component {
  state = {
    parties: this.props.parties,
  };
  render() {
    const {classes, parties, player} = this.props;
    return (
      <div className={classes.name}>
        <div>
          {player.name}
        </div>
        <div className={"circle " + player.color} />
      </div>
    )
  }
}

export default withStyles(styles)(Player);
// export default withStyles(styles)(Vote);
