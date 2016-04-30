"""
Classes example based on:
http://interactivepython.org/runestone/static/pythonds/Introduction/
ObjectOrientedProgramminginPythonDefiningClasses.html

@author Alex Sáez
"""

class LogicGate(object):

    def __init__(self, name):
        self.name = name
        self._output = None

    def connect_output_to(self, other, pin=None):
        if isinstance(other, UnaryGate):
            other._pin.connect(self)
        if isinstance(other, BinaryGate):
            if pin.lower() == 'a':
                other._pinA.connect(self)
            elif pin.lower() == 'b':
                other._pinB.connect(self)

    @property
    def output(self):
        self._output = self.perform_gate_logic()
        return self._output


class Pin(object):

    def __init__(self, name):
        self.name = name
        self._value = None
        self._connection = None

    def connect(self, gate):
        if isinstance(gate, LogicGate):
            self._connection = gate
        else:
            raise ValueError('Impossible to connect from {}'.format(gate))

    @property
    def value(self):
        if self._connection is not None:
            self._value = self._connection.output
        return self._value

    @value.setter
    def value(self, value):
        if value in (True, False, None):
            self._value = value
            if self._connection is not None:
                print('Connection broken from {} to {}'.format(
                    self._connection.name, self.name))
                self._connection = None
        else:
            raise ValueError('Not a valid input')


class BinaryGate(LogicGate):

    def __init__(self, name):
        super(BinaryGate, self).__init__(name)
        self._pinA = Pin(self.name+'_pinA')
        self._pinB = Pin(self.name+'_pinB')

    def __repr__(self):
        return "{0}.pinA: {1}\n{0}.pinB: {2}\n{0}.out: {3}\n".format(
            self.name, self._pinA._value, self._pinB._value,
            self._output)

    @property
    def pinA(self):
        return self._pinA.value

    @pinA.setter
    def pinA(self, value):
        self._pinA.value = value

    @property
    def pinB(self):
        return self._pinB.value

    @pinB.setter
    def pinB(self, value):
        self._pinB.value = value


class UnaryGate(LogicGate):

    def __init__(self, name):
        super(UnaryGate, self).__init__(name)
        self._pin = Pin(self.name+'_pin')

    def __repr__(self):
        return "{0}.pin: {1}\n{0}.out: {2}\n".format(
            self.name, self._pin._value, self._output)

    @property
    def pin(self):
        return self._pin.value

    @pin.setter
    def pin(self, value):
        self._pin.value = value


class AndGate(BinaryGate):

    def __init__(self, name):
        super(AndGate, self).__init__(name)

    def perform_gate_logic(self):
        a = self.pinA
        b = self.pinB
        if None in (a, b):
            output = None
        else:
            if (a is True) and (b is True):
                output = True
            else:
                output = False
        return output


class OrGate(BinaryGate):

    def __init__(self, name):
        super(OrGate, self).__init__(name)

    def perform_gate_logic(self):
        a = self.pinA
        b = self.pinB
        if None in (a, b):
            output = None
        else:
            if (a is True) or (b is True):
                output = True
            else:
                output = False
        return output


class NotGate(UnaryGate):

    def __init__(self, name):
        super(NotGate, self).__init__(name)

    def perform_gate_logic(self):
        if self.pin is None:
            output = None
        else:
            output = not self.pin
        return output

if __name__ == '__main__':
    g1 = AndGate('g1')
    g1.pinA = False
    g1.pinB = True
    print(g1)
    g1.output
    print(g1)

    g2 = NotGate('g2')
    g2.pin = True
    print(g2)
    g2.output
    print(g2)

    g1.connect_output_to(g2)
    print(g1, g2)

    g2.output
    print(g2)

    g1.pinA = True
    print(g1)
    print(g2)

    g2.output

    print(g1)
    print(g2)

    g2.pin = False
    g2.output
    print(g2)
