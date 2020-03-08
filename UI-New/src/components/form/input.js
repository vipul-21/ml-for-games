import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import MenuItem from '@material-ui/core/MenuItem';
import TextField from '@material-ui/core/TextField';

const styles = theme => ({
  textField: {
    marginLeft: theme.spacing.unit,
    marginRight: theme.spacing.unit,
    width: 400,
  },
});

function Input(props) {
  const { classes } = props;

  return (
    <TextField
      id={props.id}
      label={props.label}
      className={classes.textField}
      type={props.type || 'text'}
      margin="normal"
      autoFocus	={props.autoFocus}
      name={props.name}
      value={props.value}
      onChange={props.onChange}
    />
  );
}

Input.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(Input);
