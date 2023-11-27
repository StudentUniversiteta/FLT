class Node:
    def __init__(self, name, a, b):
        self.Name = name
        self.A = a
        self.B = b

class Machine:
    def __init__(self):
        self.states_list = []
        self.alphabet = []
        self.final_states = []
        self.states = []
        self.init_state = ""

    def set_states(self):
        print("Enter set of states:")
        ans = input()
        while ans != ".":
            self.states_list.append(ans)
            ans = input()


    def set_alphabet(self):
        print("Enter the input alphabet:")
        ans = input()
        while ans != ".":
            self.alphabet.append(ans)
            ans = input()

    def set_final_states(self):
        print("Enter a set of final states:")
        ans = input()
        while ans != ".":
            self.final_states.append(ans)
            ans = input()

    def set_init_state(self, init):
        self.init_state = init

    def get_note(self, name):
        for state in self.states:
            if state.Name == name:
                return state
        return None

    def is_state_exist(self, name):
        for state in self.states:
            if state and state.Name == name:
                return True
        return False

    def is_final(self, name):
        return name in self.final_states

    def is_comp(self, a, b):
        temp = ""
        if a == "":
            return b
        for i in range(len(b)):
            for j in range(len(a)):
                if b[i] == a[j]:
                    break
                if j == len(a) - 1:
                    temp += b[i]
        return temp

    def is_legal(self, name):
        if name != self.init_state and not self.is_final(name):
            for state in self.states:
                if state.Name != name:
                    if state.A == name or state.B == name:
                        return True
            return False
        else:
            return True

    def create_NFA(self, transition):
        note = None
        i = 0
        while i < len(transition):
            if transition[i] == '(':
                if not self.is_state_exist(transition[i + 1]):
                    if transition[i + 3] == 'a':
                        note = Node(transition[i + 1], transition[i + 5], "")
                    else:
                        note = Node(transition[i + 1], "", transition[i + 5])
                    self.states.append(note)
                else:
                    if transition[i + 3] == 'a':
                        self.get_note(transition[i + 1]).A += transition[i + 5]
                    else:
                        self.get_note(transition[i + 1]).B += transition[i + 5]
            i += 1

    def rebuild_to_DFA(self):
        flag = False
        temp, a, b = "", "", ""
        for state in self.states:
            if not self.is_state_exist(state.A) or not self.is_state_exist(state.B):
                if not self.is_state_exist(state.A):
                    temp = state.A
                else:
                    temp = state.B
                note = Node(temp, "", "")
                self.states.append(note)
                for char in temp:
                    a = self.get_note(char).A
                    b = self.get_note(char).B
                    self.get_note(temp).A += self.is_comp(self.get_note(temp).A, a)
                    self.get_note(temp).B += self.is_comp(self.get_note(temp).B, b)
                    self.get_note(temp).A = ''.join(sorted(self.get_note(temp).A))
                    self.get_note(temp).B = ''.join(sorted(self.get_note(temp).B))
        i = 0
        while i < len(self.states):
            if not self.is_legal(self.states[i].Name):
                del self.states[i]
                i -= 1
            i += 1

    def result(self):
        print("DFA:")
        print("Set of states:", end=' ')
        for state in self.states:
            print(state.Name, end=' ')
        print("\nInput alphabet:", end=' ')
        for char in self.alphabet:
            print(char, end=' ')
        print("\nState-transition function:")
        for state in self.states:
            for j in range(2):
                if j % 2 == 0:
                    print("D(" + state.Name + ", " + self.alphabet[0] + ") = " + state.A)
                else:
                    print("D(" + state.Name + ", " + self.alphabet[1] + ") = " + state.B)
        print("\nInitial states:", self.init_state)
        print("Final states:", end=' ')
        for state in self.states:
            for final_state in self.final_states:
                if final_state in state.Name:
                    print(state.Name, end=' ')
                    break
        print()

work = Machine()
work.set_states()
work.set_alphabet()
test = "(1,a,1) (1,a,2) (1,b,3) (2,a,2) (2,b,1) (2,b,3) (3,a,3) (3,b,3)"
work.create_NFA(test)
work.set_init_state("1")
work.set_final_states()
work.rebuild_to_DFA()
work.result()