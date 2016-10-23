"""Base class for all derived ETA objects."""


class BaseETA(object):

    """Base class for all ETA classes."""

    def __init__(self):
        """Empty initializer."""
        pass

    def update(self, time, value, max_value):
        """Update the ETA.

        Called by ProgressBar with the current time, current
        progress value and maximum value for 100% progress

        """
        raise NotImplementedError("Must be implemented in subclass")

    def get(self):
        """Get current ETA estimate.

        Queried by ProgressBar when it needed. Returns the ETA in
        seconds or None otherwise

        """
        raise NotImplementedError("Must be implemented in subclass")

    def reset(self):
        """Reset the ETA object."""
        raise NotImplementedError("Must be implemented in subclass")

    def format_eta(self, eta):
        """Convert a time elapse in seconds to hours, minutes and seconds."""
        mins, secs = divmod(eta, 60)
        hrs, mins = divmod(mins, 60)
        return list(map(int, (hrs, mins, secs)))

    @property
    def eta(self):
        """Return the unformatted ETA."""
        raise NotImplementedError("Must be implemented in subclass")
