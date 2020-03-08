import React from 'react';
import withStyles from "@material-ui/core/styles/withStyles";

import { BarChart, Bar, ReferenceLine, XAxis, YAxis, CartesianGrid, Label, Legend, Tooltip } from 'recharts';

import './barChart.css';

const styles = {
  base: {
    padding: '0em 2.25em 1.5em',
  },
  // filterName: {
  //   color: color.mediumGrey,
  //   fontSize: '0.6875em',
  //   textTransform: 'uppercase',
  //   padding: '0.75em 1em',
  // },
  // filterOption: {
  //   border: `1px solid ${color.selected}`,
  //   display: 'flex',
  //   alignItems: 'center',
  //   marginLeft: '1em',
  //
  // },
  // filter: {
  //   display: 'flex',
  //   justifyContent: 'center',
  // },
  // checkbox: {
  //   padding: '1em 0.9375em 1em 1em',
  //   borderRight: `1px solid ${color.selected}`,
  // },
  // inActiveLabel: {
  //   width: '1.75em',
  //   height: '0.125em',
  //   background: color.barChartBlue,
  //   border: `0.5px solid ${color.barChartBlue}`,
  //   borderRadius: 4,
  //   marginLeft: '1em',
  // },
  // activeLabel: {
  //   width: '1.75em',
  //   height: '0.125em',
  //   background: color.barChartPink,
  //   border: `0.5px solid ${color.barChartPink}`,
  //   borderRadius: 4,
  //   marginLeft: '1em',
  // },
  // tooltip: {
  //   background: color.darkBlue,
  //   color: color.white,
  //   padding: '1.125em',
  //   boxShadow: '0 2px 4px 0 rgba(0, 0, 0, 0.23)',
  // },
  // date: {
  //   color: color.lightBlue,
  //   fontSize: '0.675em',
  //   textAlign: 'center',
  // },
  // value: {
  //   fontSize: '0.8125em',
  //   textAlign: 'center',
  //   textTransform: 'capitalize',
  // },
};

//
//
// FilterOption.propTypes = {
//   checked: PropTypes.bool,
//   label: PropTypes.object,
//   filterName: PropTypes.string,
//   onClick: PropTypes.func,
// };
//
const CustomTooltip = (props) => {
    const { active } = props;

    if (active) {
      const { payload, label } = props;
      return (
        <div className="tooltip">
          <div>
            {payload.map((d, i) => (<div key={i} className="tooltip-value">{`${d.name}`} : {d.value}</div>))}
          </div>
          <div className="graph-label">{label}</div>
        </div>
      );
    }

    return null;
}

const FilterOption = props => (
  <div className="filter-options">
    <div className="filter-label" />
    <div className="filter-name">
      {props.filterName}
    </div>
  </div>
);

 const CustomLegend = () => (
  <div className="filter">
    <FilterOption
      filterName="Votes"
    />
  </div>
);

class CustomBarChart extends React.Component {
  render() {
    const { classes, scores  } = this.props;
    return (
      <div>
      <div className="graph">
        <BarChart
          width={730}
          height={250}
          data={scores}
        >
          <CartesianGrid strokeDasharray="0 0" vertical={false} />
        <XAxis dataKey="name" strokeWidth={2} stroke="#424242" tick={{ fontSize: 11 }} >
            <Label
              value="Votes"
              stroke="#7c7c7c"
              offset={-15}
              position="insideBottom"
            />
          </XAxis>
          <YAxis strokeWidth={2} stroke="#424242" tick={{ fontSize: 11 }} allowDecimals={false} />
        {/* <Tooltip cursor={{ fill: "#6c7a7d", fillOpacity: 0.1 }} content={<CustomTooltip />} /> */}
          <Bar dataKey="votes" fill="#FFC72C" />
        </BarChart>
      </div>
      {/* <CustomLegend /> */}
      </div>
    );
  }
}


export default withStyles(styles)(CustomBarChart);
