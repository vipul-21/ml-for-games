import React from 'react';
import { connect } from 'react-redux';
import withStyles from "@material-ui/core/styles/withStyles";
import InputLabel from "@material-ui/core/InputLabel";

import LightTheme from '../../components/background/light'
import CardAvatar from '../../components/Card/CardAvatar'
import Card from '../../components/Card/Card'
import CardBody from '../../components/Card/CardBody'
import ButtonProvider from '../../components/common/button'
import ImageProvider from '../../components/ImageProvider'
import Loader from '../../components/common/loader'
import Header from '../../components/common/header'

import first from '../../assets/first.jpg';
import second from '../../assets/second.jpg';
import logo from '../../assets/logo.png';
import dots from '../../assets/dots.svg';

import './vote.css';

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
    justifyContent: 'center',
  },
  team: {
    display: 'flex',
    alignItems: 'center',
  },
  candidateContainer: {
    display: 'flex',
  },
  candidate: {
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'center',
    padding: 10,
  },
  candidateName: {
    fontSize: '12px',
    fontWeight: '300',
    padding: '5px 0',
  },
  description: {
    textAlign: 'center',
  }

};

// TODO: Implement select design
class Vote extends React.Component {
  state = {
    parties: this.props.parties,
  };

  componentDidMount() {
    this.props.getAllParties();
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
      <div>

      <Header label="Vote On Chain"  className="logo-2" logo={logo}/>
      <LightTheme>
        <div className="vote-container">
          {/* <div className="vote-header">
            <div>
              <ImageProvider src={logo} className="logo-2"/>
            </div>
            <div>
              Vote for SC
            </div>
          </div> */}
          {this.props.parties.length == 0 ?
            <Loader />:
              <div>
                <div className="position">
                  President and Vice President
                </div>
                <div className="party-container">
                  {this.state.parties.map((party) => (
                    <Card profile>
                      <CardAvatar profile>
                          <img src={party.partyURL ? party.partyURL:first} alt="..." />
                      </CardAvatar>
                      <CardBody profile>
                        <div className={classes.cardTitle}>
                          <div className={classes.team}>{party.name}</div>
                        </div>
                        <div className={classes.candidateContainer}>
                          {/* {party.candidates.map((candidate) => (
                            <div className={classes.candidate}>
                              <div className={classes.candidateName}>{candidate}</div>
                            </div>))} */}
                        </div>
                        {/* <div className={classes.cardCategory}>{party.position}</div> */}
                        <p className={classes.description}>
                          {party.description}
                        </p>
                      </CardBody>
                      <div className="vote-btn">
                        <ButtonProvider round label="Vote" onClick={() => this.props.voteForParty(party.id)}/>
                      </div>
                    </Card>))}
                </div>
             <ImageProvider src={dots} className="dots"/>
             <div>
               <div className="position">
                 Senator
               </div>
               <div className="party-container">
                 {this.state.parties.map((party) => (
                   <Card profile>
                     <CardAvatar profile>
                         <img src={party.partyURL ? party.partyURL:first} alt="..." />
                     </CardAvatar>
                     <CardBody profile>
                       <div className={classes.cardTitle}>
                         <div className={classes.team}>{party.name}</div>
                       </div>
                       <div className={classes.candidateContainer}>
                         {/* {party.candidates.map((candidate) => (
                           <div className={classes.candidate}>
                             <div className={classes.candidateName}>{candidate}</div>
                           </div>))} */}
                       </div>
                       {/* <div className={classes.cardCategory}>{party.position}</div> */}
                       <p className={classes.description}>
                         {party.description}
                       </p>
                     </CardBody>
                     <div className="vote-btn">
                       <ButtonProvider round label="Vote" onClick={() => this.props.voteForParty(party.id)}/>
                     </div>
                   </Card>))}
                   {this.state.parties.map((party) => (
                     <Card profile>
                       <CardAvatar profile>
                           <img src={party.partyURL ? party.partyURL:first} alt="..." />
                       </CardAvatar>
                       <CardBody profile>
                         <div className={classes.cardTitle}>
                           <div className={classes.team}>{party.name}</div>
                         </div>
                         <div className={classes.candidateContainer}>
                           {/* {party.candidates.map((candidate) => (
                             <div className={classes.candidate}>
                               <div className={classes.candidateName}>{candidate}</div>
                             </div>))} */}
                         </div>
                         {/* <div className={classes.cardCategory}>{party.position}</div> */}
                         <p className={classes.description}>
                           {party.description}
                         </p>
                       </CardBody>
                       <div className="vote-btn">
                         <ButtonProvider round label="Vote" onClick={() => this.props.voteForParty(party.id)}/>
                       </div>
                     </Card>))}

               </div>
             </div>
             <ImageProvider src={dots} className="dots"/>
           </div>
          }

        </div>
      </LightTheme>
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
    }
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(withStyles(styles)(Vote));
// export default withStyles(styles)(Vote);
