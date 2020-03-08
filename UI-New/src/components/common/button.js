import React from 'react';
import PropTypes from 'prop-types';

import { withStyles } from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';
import Fab from '@material-ui/core/Fab';

const styles = theme => ({
  button: {
    margin: theme.spacing.unit,
    background: '#1b2e43',
    '&:hover': {
      background: '#1b2e43'
    }
  },
});

function ButtonProvider(props) {
  const { classes, label, round, onClick,type } = props;

  return (
    round ?
    <Fab
      variant="extended"
      size="medium"
      color="primary"
      aria-label="Add"
      className={classes.button}
      onClick={onClick}
      type={type}
    >
      {label}
    </Fab> :
    <Button
      variant="raised"
      color="primary"
      className={classes.button}
      onClick={onClick}
      type={type}

    >
      {label}
    </Button>
  );
}

ButtonProvider.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(ButtonProvider);
