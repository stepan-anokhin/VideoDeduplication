import React, { useMemo } from "react";
import clsx from "clsx";
import PropTypes from "prop-types";
import FileType from "../../../prop-types/FileType";
import PreviewContainer from "./PreviewContainer";
import PreviewHeader from "./PreviewHeader";
import PreviewDivider from "./PreviewDivider";
import PreviewFileAttributes from "./PreviewFileAttributes";
import Distance from "../../../../common/components/Distance";
import { localAttributes } from "./attributes";
import PreviewMainAction from "./PreviewMainAction";
import { routes } from "../../../../routing/routes";
import { useIntl } from "react-intl";
import { useHistory } from "react-router-dom";
import InactiveIcon from "@material-ui/icons/NotInterestedOutlined";
import VideocamOutlinedIcon from "@material-ui/icons/VideocamOutlined";
import MatchAPI from "../../../../application/match/MatchAPI";
import FileMatchType from "../../../../application/match/prop-types/FileMatchType";

import { makeStyles } from "@material-ui/styles";

const useStyles = makeStyles((theme) => ({
  falsePositive: {
    backgroundColor: theme.palette.backgroundInactive,
  },
}));

/**
 * Get translated text
 */
function useMessages() {
  const intl = useIntl();
  return {
    caption: intl.formatMessage({ id: "file.attr.name" }),
    compare: intl.formatMessage({ id: "actions.compare" }),
    showDetails: intl.formatMessage({ id: "actions.showFileDetails" }),
    delete: intl.formatMessage({ id: "actions.delete" }),
    restore: intl.formatMessage({ id: "actions.restore" }),
  };
}

/**
 * Get delete action.
 */
function useToggleFalsePositive({ match, messages }) {
  const matchAPI = MatchAPI.use();
  return useMemo(
    () => ({
      title: match.falsePositive ? messages.restore : messages.delete,
      handler: async () => {
        const updated = { ...match, falsePositive: !match.falsePositive };
        await matchAPI.updateFileMatch(updated, match);
      },
    }),
    [matchAPI, match.id, match.falsePositive]
  );
}

/**
 * Get comparison action.
 */
function useCompare({ match, motherFile, messages }) {
  const history = useHistory();
  return useMemo(
    () => ({
      title: messages.compare,
      handler: () =>
        history.push(
          routes.collection.fileComparisonURL(motherFile?.id, match.file?.id)
        ),
    }),
    [match.file?.id, motherFile?.id]
  );
}

/**
 * Get "Show Details" action.
 */
function useShowDetails({ match, messages }) {
  const history = useHistory();
  return useMemo(
    () => ({
      title: messages.showDetails,
      handler: () => history.push(routes.collection.fileURL(match.file.id)),
    }),
    [match.file.id]
  );
}

function useActions({ match, motherFile, messages }) {
  const compare = useCompare({ match, motherFile, messages });
  const showDetails = useShowDetails({ match, messages });
  const toggleFalsePositive = useToggleFalsePositive({ match, messages });
  const list = useMemo(() => {
    if (motherFile.external) {
      return [showDetails];
    }
    return [showDetails, toggleFalsePositive, compare];
  }, [showDetails, toggleFalsePositive, compare, motherFile.external]);

  return {
    compare,
    showDetails,
    toggleFalsePositive,
    list,
  };
}

function LocalMatchPreview(props) {
  const { motherFile, match, highlight, className, ...other } = props;
  const classes = useStyles();
  const messages = useMessages();
  const actions = useActions({ match, motherFile, messages });

  const mainAction = motherFile?.external
    ? actions.showDetails
    : actions.compare;

  const Icon = match.falsePositive ? InactiveIcon : VideocamOutlinedIcon;

  return (
    <PreviewContainer
      className={clsx(match.falsePositive && classes.falsePositive, className)}
      {...other}
    >
      <PreviewHeader
        text={match.file.filename}
        highlight={highlight}
        caption={messages.caption}
        icon={Icon}
        actions={actions.list}
      />
      <PreviewDivider dark={match.falsePositive} />
      <PreviewFileAttributes file={match.file} attrs={localAttributes} />
      <PreviewDivider dark={match.falsePositive} />
      <Distance value={match.distance} />
      <PreviewDivider dark={match.falsePositive} />
      <PreviewMainAction name={mainAction.title} onFire={mainAction.handler} />
    </PreviewContainer>
  );
}

LocalMatchPreview.propTypes = {
  /**
   * Mother file
   */
  motherFile: FileType.isRequired,
  /**
   * Match details
   */
  match: FileMatchType.isRequired,
  /**
   * File name substring to highlight
   */
  highlight: PropTypes.string,
  className: PropTypes.string,
};

export default LocalMatchPreview;
