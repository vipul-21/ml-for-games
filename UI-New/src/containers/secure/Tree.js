import React from 'react';
import { connect } from 'react-redux';

import withStyles from "@material-ui/core/styles/withStyles";
import InputLabel from "@material-ui/core/InputLabel";

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
import { ForceGraph3D } from 'react-force-graph';

import tick from '../../assets/tick.svg';

import './Tree.css';
const data = [
  {
    "name": "Page A",
    "uv": 4000,
    "pv": 2400,
    "amt": 2400
  },
  {
    "name": "Page B",
    "uv": 3000,
    "pv": 1398,
    "amt": 2210
  },
  {
    "name": "Page C",
    "uv": 2000,
    "pv": 9800,
    "amt": 2290
  },
  {
    "name": "Page D",
    "uv": 2780,
    "pv": 3908,
    "amt": 2000
  },
  {
    "name": "Page E",
    "uv": 1890,
    "pv": 4800,
    "amt": 2181
  },
  {
    "name": "Page F",
    "uv": 2390,
    "pv": 3800,
    "amt": 2500
  },
  {
    "name": "Page G",
    "uv": 3490,
    "pv": 4300,
    "amt": 2100
  }
]

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
  tooltip:{
    backgroundColor: '#1b2e43',
    color: '#fff',
    padding: '16px',
    boxShadow: '0 2px 4px 0 rgba(0, 0, 0, 0.23)',
    fontSize: '14px',
    textAlign: "center",

  },


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

class Tree extends React.Component {
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
  }
  componentDidMount(){
    this.props.getZetaData();
  }


  render() {
    const { classes, feedbackUrl,zetaData, feedbackMessage } = this.props;
    const data = {
        nodes: [{ id: 'Harry' }, { id: 'Sally' }, { id: 'Alice' }],
        links: [{ source: 'Harry', target: 'Sally' }, { source: 'Sally', target: 'Alice' }]
    };
    const colors = ["#040a55", "#1e2bd7", "#2876d7", "#55b8f3", "#80ecf7"]
    const nodeColor = []
    if(zetaData) {
      zetaData.links.map((link) => {
        nodeColor[link.target] = link.weight
      })
      nodeColor['0x821aEa9a577a9b44299B9c15c88cf3087F3b5544'.toLowerCase()] = 0


    }
    console.log(nodeColor);
    return (
      <LightTheme>
          <div className="admin-container">

          <LeftPanel/>
          <div  className="right-panel">

        <Header label="Tree Structure" logo={logo}/>
          <Card>
            <div className="vote-header">
              <div>ZETA tree for malicious node - Address : 0x821aea9a577a9b44299b9c15c88cf3087f3b5544</div>
            </div>
            {zetaData ?                        <ForceGraph3D
                        ref={el => { this.fg = el; }}
                        width={1000}
                        height={400}
                        nodeOpacity={1}
                        nodeColor={d => colors[nodeColor[d.id]]}

                        enableNodeDrag={false}
                        graphData={zetaData}
                        linkDirectionalArrowLength={4}
                        linkCurvature={0.25}
                        backgroundColor={"#fff"}
                        linkDirectionalArrowColor={"#1b2e43"}
                        linkColor={"#1b2e43"}
                        linkOpacity={"1"}
                        nodeLabel={d => {return `<div class=${classes.tooltip}>Address : ${d.id}`}}
                        />: ''}
          </Card>
        </div>
      </div>

      </LightTheme>)
    }
}

const mapStateToProps = state => {
  return {
     zetaData: state.main.zetaData,
     feedbackMessage: state.main.feedbackMessage
    };
};

const mapDispatchToProps = (dispatch) => {
  return {
    getZetaData: () => {
      dispatch({ type: 'GET_ZETA_INIT' })
    },
  }
}


export default connect(mapStateToProps, mapDispatchToProps)(withStyles(styles)(Tree));
