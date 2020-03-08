import React from 'react';
import { connect } from 'react-redux';

import withStyles from "@material-ui/core/styles/withStyles";
import InputLabel from "@material-ui/core/InputLabel";
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ReferenceLine,
} from 'recharts';

import LightTheme from '../../components/background/light'
import CardAvatar from '../../components/Card/CardAvatar'
import Card from '../../components/Card/Card'
import CardBody from '../../components/Card/CardBody'
import ImageProvider from '../../components/ImageProvider'
import Input from '../../components/form/input'
import CustomLink from '../../components/navigation/link'
import ButtonProvider from '../../components/common/button'
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import LeftPanel from './admin/components/leftPanel'
import Header from '../../components/common/header'
import logo from '../../assets/dashboard.svg';
// import CustomBarChart from '../../components/graph/barChart'

import tick from '../../assets/tick.svg';

import './MalicousNode.css';


//
// <LineChart width={730} height={250} data={data}
//   margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
//   <XAxis dataKey="name" />
//   <YAxis />
//   <CartesianGrid strokeDasharray="3 3" />
//   <Tooltip />
//   <Legend verticalAlign="top" height={36}/>
//   <Line name="pv of pages" type="monotone" dataKey="pv" stroke="#8884d8" />
//   <Line name="uv of pages" type="monotone" dataKey="uv" stroke="#82ca9d" />
// </LineChart>

const styles = {
  cardCategoryWhite: {
    color: "rgba(255,255,255,.62)",
    margin: "0",
    fontSize: "14px",
    marginTop: "0",
    marginBottom: "0"
  },
  cardTitleWhite: {
    color: "#FFFFFF",
    marginTop: "0px",
    minHeight: "auto",
    fontWeight: "300",
    fontFamily: "'Roboto', 'Helvetica', 'Arial', sans-serif",
    marginBottom: "3px",
    textDecoration: "none"
  },
  root: {
    width: '100%',
    overflowX: 'auto',
    zIndex: 1,
  },
  table: {
    minWidth: 700,
  },
  ip: {
    display: "flex",
    alignItems: "baseline",
    padding: "20px"
  }
};

let id = 0;
function createData(name, calories, fat, carbs, protein) {
  id += 1;
  return { id, name, calories, fat, carbs };
}

const rows = [
  createData('Frozen yoghurt', 159, 6.0, 24, 4.0),
  createData('Ice cream sandwich', 237, 9.0, 37, 4.3),
  createData('Eclair', 262, 16.0, 24, 6.0),
  createData('Cupcake', 305, 3.7, 67, 4.3),
  createData('Gingerbread', 356, 16.0, 49, 3.9),
];

class MalicousNode extends React.Component {
  state = {
    address: ""
  }
  onChange = (event) => {
    this.setState({
      address: event.target.value
    })
  }
  onClick = () => {
    const { address } = this.state;
    this.props.getMalicious(address);
  }



  render() {
    const { classes, feedbackUrl, malicious } = this.props;
    const scores =[ {
      name: 'a',
      value: 1
    },
    {
     name: 'b',
     value: 2
   }]

    return (
      <LightTheme>
          <div className="admin-container">

          <LeftPanel/>
            <div className="right-panel">

        <Header label="Malicious Data" logo={logo}/>
          <Card>
            <div className="vote-header">
              <div>Search for history</div>
            </div>

            <form onSubmit={(e) => {e.preventDefault(); this.onClick(e)}}>
              <div className={classes.ip}>
                <Input
                   id="address" name="address" value={this.state.address}
                   label="Enter the address" autoFocus onChange={this.onChange}
                  />
                  <div>
                    <ButtonProvider type="submit" label="Get the zeta graph" onClick={this.onClick}/>
                  </div>

              </div>

            </form>
            {malicious ?
            <LineChart width={800} height={300} data={malicious}>
              <XAxis dataKey="zeta" padding={{ left: 30, right: 30 }} />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="value" stroke="#82ca9d" />
            </LineChart> : ''}
          </Card>
        </div>
      </div>
      </LightTheme>)
    }
}

const mapStateToProps = state => {
  return {
     malicious: state.main.malicious,
     feedbackMessage: state.main.feedbackMessage
    };
};

const mapDispatchToProps = (dispatch) => {
  return {
    getMalicious: (address) => {
      dispatch({ type: 'GET_MALICIOUS_INIT', address })
    },
  }
}


export default connect(mapStateToProps, mapDispatchToProps)(withStyles(styles)(MalicousNode));
