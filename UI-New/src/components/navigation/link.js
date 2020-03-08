import React from 'react';
import { Link } from 'react-router-dom';
import PropTypes from 'prop-types';

const CustomLink = (props) => {
  return (
    <Link to={props.to}>
      {props.children}
    </Link>
  );
}

CustomLink.propTypes = {
  to: PropTypes.string.isRequired,
};

export default CustomLink;
