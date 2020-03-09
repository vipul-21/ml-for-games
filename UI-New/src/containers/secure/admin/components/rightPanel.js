import React from 'react';
import { connect } from 'react-redux';
import withStyles from "@material-ui/core/styles/withStyles";
import InputLabel from "@material-ui/core/InputLabel";
import { InteractiveForceGraph,ForceGraph, ForceGraphNode, ForceGraphLink } from 'react-vis-force';
import { ForceGraph3D } from 'react-force-graph';
import ButtonProvider from '../../../../components/common/button'
import {
  BarChart, Bar, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
} from 'recharts';

// import CardAvatar from '../../components/Card/CardAvatar'
import Card from '../../../../components/Card/Card'
// import CardBody from '../../components/Card/CardBody'
import CustomBarChart from '../../../../components/graph/barChart'
import Header from '../../../../components/common/header'
import ImageProvider from '../../../../components/ImageProvider'
import Loader from '../../../../components/common/loader'
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';

// import first from '../../assets/first.jpg';
// import second from '../../assets/second.jpg';
import logo from '../../../../assets/dashboard.svg';
import map from '../../../../assets/map_large_1.jpg';
import ghost from '../../../../assets/ghost_1.png';
const colors = ["#040a55", "#1e2bd7", "#2876d7", "#55b8f3", "#80ecf7"]
import './rightPanel.css';
import mapJson from '../../map.js';
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
  root: {
    width: '900px',
    overflowX: 'auto',
    zIndex: 1,
    textAlign: 'center',
    margin:'15px auto'
  },
  table: {
    width: '100%',
    tableLayout: 'fixed',
   },
  tooltip:{
    backgroundColor: '#1b2e43',
    color: '#fff',
    padding: '16px',
    boxShadow: '0 2px 4px 0 rgba(0, 0, 0, 0.23)',
    fontSize: '14px',
    textAlign: "center",

  },
  label: {
    color: "#779fcb",
    fontSize: "12px",
    textAlign: "center",
    paddingTop: "2px",

  },
  zeta:{
    fontWeight:600,
  },
  button:{
    textAlign: 'center'
  },
  graph2: {
    display: 'flex',
    justifyContent: 'center'
  },
  map : {
    display: 'block',
    margin: "30px",
    background: "url("+map+ ")",
    width: "2570px",
    height: "1926px"
  }

};

// TODO: Implement select design
class RightPanel extends React.Component {
  state = {
    ghostList: []
  };
  _handleClick = node => {
  // Aim at node from outside it
  const distance = 40;
  const distRatio = 1 + distance/Math.hypot(node.x, node.y, node.z);
  this.fg.cameraPosition(
    { x: node.x * distRatio, y: node.y * distRatio, z: node.z * distRatio }, // new position
    node, // lookAt ({ x, y, z })
    3000  // ms transition duration
  );
}


  componentDidMount() {
      // var canvas = document.getElementById('map');
      // var context = canvas.getContext('2d');
      var that = this;
      // canvas.addEventListener('mousemove', function(evt) {
      //   var mousePos = that.getMousePos(canvas, evt);
      //   var message = 'Mouse position: ' + mousePos.x + ',' + mousePos.y;
      //   console.log("message: ", mousePos.x + ',' + mousePos.y);
      //   that.writeMessage(canvas, message);
      // }, false);
      // this.createCircle();
      // console.log(firebase);
      var playerA = firebase.database().ref('ghostbuster/a');
      playerA.on('value', function(snapshot) {
        that.updatePosition("a", snapshot.val())
      });
      var playerB = firebase.database().ref('ghostbuster/b');
      playerB.on('value', function(snapshot) {
        that.updatePosition("b", snapshot.val())
      });
      var playerC = firebase.database().ref('ghostbuster/c');
      playerC.on('value', function(snapshot) {
        that.updatePosition("c", snapshot.val())
      });
      var playerD = firebase.database().ref('ghostbuster/d');
      playerD.on('value', function(snapshot) {
        that.updatePosition("d", snapshot.val())
      });
      var playerE = firebase.database().ref('ghostbuster/e');
      playerE.on('value', function(snapshot) {
        that.updatePosition("e", snapshot.val())
      });
      var ghost = firebase.database().ref('ghostbuster/ghost');
      ghost.on('value', function(snapshot) {
        that.updatePosition("ghost", snapshot.val())
      });

  }

  writeMessage = (canvas, message) => {
    var context = canvas.getContext('2d');
    context.clearRect(0, 0, canvas.width, canvas.height);
    context.font = '30pt Calibri';
    context.fillStyle = 'black';
    context.fillText(message, 10, 25);

  }

  createCircle = (posX, posY, color, ply) => {

    var c = document.getElementById("map");
    var ctx = c.getContext("2d");

    if (ply == "ghost") {
      var base_image = new Image();
base_image.src = ghost;
base_image.onload = function(){
  ctx.drawImage(base_image, posX-30, posY-30);
}

    } else {
      ctx.beginPath();
      ctx.arc(posX, posY, 30,  0, 2 * Math.PI);
      ctx.lineWidth = 10;
      ctx.fillStyle = color;
      ctx.fill();
      ctx.strokeStyle = color;
      ctx.stroke();

    }
  }
  clearLast = (player) => {
    var c = document.getElementById("map");
    var ctx = c.getContext("2d");
    var posX = -1;
    var posY = -1;
    switch (player) {
      case "a": {
        if (this.state.a) {
        posX = this.state.a[0];
        posY = this.state.a[1];
      }
        break;
      }
      case "b": {
        if (this.state.b) {

        posX = this.state.b[0];
        posY = this.state.b[1];
      }
        break;
      }
      case "c": {
        if (this.state.c) {

        posX = this.state.c[0];
        posY = this.state.c[1];
      }
        break;
      }
      case "d": {
        if (this.state.d) {

        posX = this.state.d[0];
        posY = this.state.d[1];
      }
        break;
      }
      case "e": {
        if (this.state.e) {

        posX = this.state.e[0];
        posY = this.state.e[1];
      }
        break;
      }
      case "ghost": {
        if (this.state.ghost) {

        posX = this.state.ghost[0];
        posY = this.state.ghost[1];
      }
        break;
      }
      default:
        break;
    }

    console.log("player",player, posX, posY);
    if (posX != - 1 && posY != -1) {
      ctx.clearRect(posX-40, posY-40, posX+40, posX+40);
    }

  }
  updatePosition = (player, value) => {
    console.log(player, value);
    switch (player) {
      case "a": {
        console.log(value, mapJson[value.toString()]);
        var posX = mapJson[value.toString()][0];
        var posY = mapJson[value.toString()][1];
        this.clearLast('a')
        this.setState({
          a: [posX, posY]
        })
        this.createCircle(posX, posY, "#c71b1b")
        break;
      }
      case "b": {
        var posX = mapJson[value.toString()][0];
        var posY = mapJson[value.toString()][1];
        this.clearLast('b')
        this.setState({
          b: [posX, posY]
        })
        this.createCircle(posX, posY, "#fbff00")
        break;
      }
      case "c": {
        var posX = mapJson[value.toString()][0];
        var posY = mapJson[value.toString()][1];
        this.clearLast('c')

        this.setState({
          c: [posX, posY]
        })
        this.createCircle(posX, posY, "#00dcff")
        break;
      }
      case "d": {
        var posX = mapJson[value.toString()][0];
        var posY = mapJson[value.toString()][1];
        this.clearLast('d')
        this.setState({
          d: [posX, posY]
        })
        this.createCircle(posX, posY, "#00ff08")
        break;
      }
      case "e": {
        var posX = mapJson[value.toString()][0];
        var posY = mapJson[value.toString()][1];
        this.clearLast('e')

        this.setState({
          e: [posX, posY]
        })
        this.createCircle(posX, posY, "#fb00ff")
        break;
      }
      case "ghost": {
        var posX = mapJson[value.toString()][0];
        var posY = mapJson[value.toString()][1];
        this.clearLast('ghost')

        this.setState({
          ghost: [posX, posY]
        })
        this.createCircle(posX, posY, "#000", "ghost")
        break;
      }

      default:

    }
  }



  render() {
    const {classes, scores, result, maliciousData, lastUpdated, flow} = this.props;
    console.log(result, maliciousData, scores, flow);
    const GROUPS = 12;
    let data= {}
    let newData = []
    if(flow && scores) {
      console.log("her",data)

      Object.keys(flow).map((key, i) => {
        if(data[scores[key.toLowerCase()]] == undefined) {
          data[scores[key.toLowerCase()]] = [flow[key].fromCount - flow[key].toCount];
        } else {
          data[scores[key.toLowerCase()]].push(flow[key].fromCount - flow[key].toCount);
        }
    });

    Object.keys(data).map((key, i) => {
      var numbers = data[key] // sums to 100
      var sum = 0;
      for (var i = 0; i < numbers.length; i++) {
        sum += numbers[i]
      }
      newData.push({value: key, withheld: sum})});
    console.log("her",data,newData)

  }




    return (
      <div className="right-panel">
        <Card className={classes.map}>
          <canvas id="map" width="2570" height="1926"></canvas>
        </Card>
      </div>
    )

    }
}

export default (withStyles(styles)(RightPanel));
