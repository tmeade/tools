from abc import ABCMeta, abstractmethod
import maya.cmds as mc

VALID_SIDE_NAMES = ['lt', 'rt', 'ctr']
VALID_RIG_TYPES = ['ctrl', 'joint', 'grp', 'offset', 'ikHandle', 'locator']
VALID_MAYA_NODE_TYPES = mc.ls(nt=True)


class NameBase(object):
    '''Base class for returning the proper string and object name of a valid rig name.
    parameters (string): The name to be processed.
    returns (string): String representation of valid name element.
    '''
    # Python 2.7.x hack to implement abstractmethod.  Otherwise, imort ABC and inherit like:
    #   class NameBase(ABC)
    __metaclass__ = ABCMeta

    def __init__(self, name=None):
        self.name = name
        self.validate()
        self.cleanup()

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return "{}('{}')".format(self.__class__.__name__, self.name)

    @abstractmethod
    def validate(self):
        return

    @abstractmethod
    def cleanup(self):
        return


class Side(NameBase):
    def __init__(self, name):
        super(Side, self).__init__(name)

    def validate(self):
        assert self.name in VALID_SIDE_NAMES, 'Side name must match {}!'.format(VALID_SIDE_NAMES)

    def cleanup(self):
        return self.name


class Base(NameBase):
    def __init__(self, name):
        super(Base, self).__init__(name)

    def validate(self):
        assert isinstance(self.name, str), 'Base name must be an string!'
        return self.name()

    def cleanup(self):
        self.name = self.name.lower()


class Region(NameBase):
    pass


class Position(NameBase):
    def __init__(self, name, padding=1):
        self.padding = padding
        super(Position, self).__init__(name)

    def validate(self):
        try:
            int(self.name)
            assert isinstance(self.name, (int, str)), 'Position must be an integer or string!'
        except (ValueError, AssertionError), e:
            print 'Position must be a numnerical!', e

    def cleanup(self):
        self.name = '{value:0{pad}d}'.format(value=int(self.name), pad=self.padding)


class NodeType(NameBase):
    pass


class Name(NameBase):
    def __init__(
                self,
                name=None,
                side=None,
                base=None,
                region=None,
                position=None,
                nodeType=None):
        self.name = name,
        self.side = side,
        self.base = base,
        self.region = region,
        self.position = position,
        self.nodeType = nodeType

    def validate(self):
        # This should validate each item passed in to see if it is either a proper object type or
        # validate it's input.
        #
        # We should be able to validate self.name on it's own so that the  user could type in a
        # complete string name without having to set all of the variables?
        #
        # If the pass in  name then we should leave the others to override that???  Might be nice
        # for mirroring?
        return

    def cleanup(self):
        # This will probably execute the basic logic to construct the name.  It  might look like:
        # Side_Base_Region_Position_NodeType

        # Side, Region, and Position could be optional?
        return
