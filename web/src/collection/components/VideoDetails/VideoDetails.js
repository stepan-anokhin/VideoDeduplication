import React, { useCallback, useState } from "react";
import clsx from "clsx";
import PropTypes from "prop-types";
import { makeStyles } from "@material-ui/styles";
import { useParams } from "react-router-dom";
import { useIntl } from "react-intl";
import Paper from "@material-ui/core/Paper";
import Button from "../../../common/components/Button";
import Grid from "@material-ui/core/Grid";
import VideoPlayerPane from "./VideoPlayerPane";
import VideoInformationPane from "./VideoInformationPane";
import { randomFile } from "../../../server-api/MockServer/fake-data/files";
import { seekTo } from "./seekTo";
import VideoDetailsHeader from "./VideoDetailsHeader";

const useStyles = makeStyles((theme) => ({
  root: {
    display: "flex",
    flexDirection: "column",
    alignItems: "stretch",
    padding: theme.dimensions.content.padding,
    paddingTop: theme.dimensions.content.padding * 2,
  },
  actions: {
    display: "flex",
    justifyContent: "flex-end",
    alignItems: "center",
    padding: theme.spacing(2),
  },
  header: {
    margin: theme.spacing(2),
  },
  dataContainer: {
    padding: theme.spacing(2),
  },
}));

/**
 * Get i18n messages
 */
function useMessages() {
  const intl = useIntl();
  return {
    compare: intl.formatMessage({ id: "actions.compare" }),
  };
}

const file = randomFile();

function VideoDetails(props) {
  const { className } = props;
  const messages = useMessages();
  const { id } = useParams();
  const [player, setPlayer] = useState(null);
  const classes = useStyles();

  const handleJump = useCallback(seekTo(player, file), [player, file]);

  return (
    <div className={clsx(classes.root, className)}>
      <div className={classes.actions}>
        <Button color="primary" variant="contained">
          {messages.compare}
        </Button>
      </div>
      <VideoDetailsHeader file={file} className={classes.header} />
      <div className={classes.dataContainer}>
        <Grid container spacing={5}>
          <Grid item xs={12} lg={6}>
            <VideoPlayerPane file={file} onPlayerReady={setPlayer} />
          </Grid>
          <Grid item xs={12} lg={6}>
            <VideoInformationPane file={file} onJump={handleJump} />
          </Grid>
        </Grid>
      </div>
    </div>
  );
}

VideoDetails.propTypes = {
  className: PropTypes.string,
};

export default VideoDetails;