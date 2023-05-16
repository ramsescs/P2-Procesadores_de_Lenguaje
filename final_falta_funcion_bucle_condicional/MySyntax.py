from MyLexer import MyLexer
#from myLexer import tokens
 # Build the lexer and try it out
import ply.yacc as yacc
import copy

class MySyntax(object):
    m = MyLexer()
    tokens = m.tokens

    tipo = ""

    def __init__(self, input):
        print("Construyendo MySyntax")
        self.a = 3
        self.names = []
        self.tablaSimbolos = {}
        self.funciones = {}
        self.variables = {}

        self.variablesI = {}
        self.registros = {}
        self.vectores = {}
        self.funcionesL = []
        self.variablesL = []
        self.registrosL = []
        self.vectoresL = []

        yacc.yacc(module=self)
        yacc.parse(input)

    def p_statements(self, p):
        '''statements : statement FINPARRAFO statements
                      | expresion FINPARRAFO statements
                      |
                      '''
        # Agrega la acción semántica aquí

    def p_statements1(self, p):
        '''statements1 : statement FINPARRAFO statements1
                        |'''

    # Agrega la acción semántica aquí

    def p_statement(self, p):
        '''statement : asignacion
                     | def_funcion
                     | condicional
                     | bucle
                     | declaracion
                     | declaracion_reg
                     | declaracion_vec
                     | '''

    def p_declaracion(self, p):
        '''declaracion : tipo NAME '=' expresion
                       | tipo varios_name
                       '''

        if len(p) == 5:
            self.check_and_assign_variable(p[1].upper(), p[2], p[4])

        elif len(p) == 3:
            names = p[2].split(',')
            if p[1].upper() in ['ENTERO', 'REAL', 'BOOLEANO', 'CARACTER']:
                valor = 0 if p[1].upper() == 'ENTERO' else 0.0 if p[1].upper() == 'REAL' else False if p[
                                                                                                           1].upper() == 'BOOLEANO' else ''
                for name in names:
                    self.check_and_assign_variable(p[1].upper(), name, valor)

            elif p[1].upper() in self.registros:
                for name in names:
                    self.check_and_assign_variable(p[1].upper(), name, copy.deepcopy(self.registros[p[1]]), True)

    def p_varios_name(self, p):
        '''varios_name : NAME ',' varios_name
                       | NAME '''
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 4:
            p[0] = p[1] + ',' + p[3]

        print("p_varios_name", p[0])

    def p_tipo(self, p):
        '''tipo : ENTERO
                | REAL
                | BOOLEANO
                | CARACTER
                | NAME'''
        p[0] = p[1].upper()
        print("p_tipo", p[0])


    def p_declaracion_reg(self, p):
        '''declaracion_reg : REGISTRO NAME '{' blq_registro '}' '''
        if p[2] not in self.names:
            self.names.append(p[2])
            self.registros[p[2]] = p[4]
        else:
            print("ERROR6: Variable ", p[2], " ya declarada")

    def p_blq_registro(self, p):
        '''blq_registro : tipo varios_name ';' FINPARRAFO blq_registro
                        | tipo varios_name ';'
                        | VECTOR tipo_VECTOR NAME '[' NUMINTEGER ']' ';' FINPARRAFO blq_registro
                        | VECTOR tipo_VECTOR NAME '[' NUMINTEGER ']' ';' '''
        valor = 0 if p[1].upper() == 'ENTERO' or p[2].upper() == 'ENTERO' else \
            0.0 if p[1].upper() == 'REAL' or p[2].upper() == 'REAL' else \
                False if p[1].upper() == 'BOOLEANO' or p[2].upper() == 'BOOLEANO' else ''

        if len(p) in [4, 6]:
            if p[1].upper() in ['ENTERO', 'REAL', 'BOOLEANO', 'CARACTER']:
                p[0] = self.assign_values(p[1], p[2], valor, p[5] if len(p) == 6 else None)
            elif p[1] in self.registros:
                p[0] = self.assign_values(p[1], p[2], copy.deepcopy(self.registros[p[1]]),
                                          p[5] if len(p) == 6 else None)
            else:
                print("ERROR: No existe el REGISTRO ", p[2], " que desea utilizar")

        elif len(p) in [8, 10]:
            if ',' not in p[2]:
                lista = [valor for _ in range(p[5])]
                p[0] = {p[3]: {'tipo': p[2], 'tam': p[5], 'valor': lista}}
            else:
                print("ERROR: No se puede inicializar varios vectores de esta manera")

        print('p_blq_registro', p[0])


    def p_tipo_VECTOR (self,p):
        '''tipo_VECTOR : ENTERO
                        | REAL
                        | BOOLEANO
                        | CARACTER'''
        p[0] = p[1]

    def p_declaracion_vec(self, p):
        '''declaracion_vec : VECTOR tipo_VECTOR NAME '[' NUMINTEGER ']' '''

        lista = []
        if p[2].upper() == 'ENTERO':
            for i in range(p[5]):
                lista.append(0)
        elif p[2].upper() == 'REAL':
            for i in range(p[5]):
                lista.append(0.0)
        elif p[2].upper() == 'BOOLEANO':
            for i in range(p[5]):
                lista.append(False)
        elif p[2].upper() == 'CARACTER':
            for i in range(p[5]):
                lista.append('')

        if p[3] not in self.names:
            self.vectores[p[3]] = {'tipo': p[2],
                                   'tam': p[5],
                                   'valor': lista}
            self.names.append(p[3])
        else:
            print("ERROR11: Variable ", p[3]," ya declarada")




    def p_asignacion(self, p):
        '''asignacion : name_chain '=' expresion
                      | name_chain '[' expresion ']' '=' expresion'''


        if '.' not in p[1] and len(p) == 4:
            if p[1] in self.variables:
                if self.variables[p[1]]['tipo'].upper() == 'ENTERO' and type(p[3]) == int or self.variables[p[1]]['tipo'].upper() == 'REAL' and type(p[3]) == float \
                        or self.variables[p[1]]['tipo'].upper() == 'BOOLEANO' and type(p[3]) == bool or self.variables[p[1]]['tipo'].upper() == 'CARACTER' and type(
                    p[3]) == str:
                    self.variables[p[1]]['valor'] = p[3]
                elif self.variables[p[1]]['tipo'].upper() == 'ENTERO' and type(p[3]) == str:
                    self.variables[p[1]]['valor'] = ord(p[3])

                elif self.variables[p[1]]['tipo'].upper() == 'REAL' and type(p[3]) == int:
                    self.variables[p[1]]['valor'] = float(p[3])

                else:
                    print("ERROR12: Tipo incorrecto")
            else:
                print("ERROR13: Variable ", p[1], "no declarada")
        elif '.' in p[1] and len(p) == 4:
            names = p[1].split('.')
            name = self.variables[names[0]]
            for a in range(1,len(names)):
                if names[a] in name['valor']:
                    name = name['valor'][names[a]]
                else:
                    print("ERROR14: Variable ", names[a], "no está en el registro", name['tipo'])

            if name['tipo'].upper() == 'ENTERO' and type(p[3]) == int or name[
                'tipo'].upper() == 'REAL' and type(p[3]) == float \
                    or name['tipo'].upper() == 'BOOLEANO' and type(p[3]) == bool or \
                    name['tipo'].upper() == 'CARACTER' and type(
                p[3]) == str:
                name['valor'] = p[3]
            elif name['tipo'].upper() == 'ENTERO' and type(p[3]) == str:
                name['valor'] = ord(p[3])

            elif name['tipo'].upper() == 'REAL' and type(p[3]) == int:
                name['valor'] = float(p[3])

            else:
                print("ERROR15: Tipo incorrecto")


        elif '.' not in p[1] and len(p)==7:
            if p[1] in self.vectores:
                if type(p[3]) == int and p[3]<self.vectores[p[1]]['tam']:
                    if self.vectores[p[1]]['tipo'].upper() == 'ENTERO' and type(p[6]) == int or self.vectores[p[1]][
                        'tipo'].upper() == 'REAL' and type(p[6]) == float \
                            or self.vectores[p[1]]['tipo'].upper() == 'BOOLEANO' and type(p[6]) == bool or \
                            self.vectores[p[1]]['tipo'].upper() == 'CARACTER' and type(
                        p[3]) == str:
                        self.vectores[p[1]]['valor'][p[3]] = p[6]
                    elif self.vectores[p[1]]['tipo'].upper() == 'ENTERO' and type(p[6]) == str:
                        self.vectores[p[1]]['valor'][p[3]] = ord(p[6])

                    elif self.vectores[p[1]]['tipo'].upper() == 'REAL' and type(p[6]) == int:
                        self.vectores[p[1]]['valor'][p[3]] = float(p[6])

                    else:
                        print("ERROR16: Tipo incorrecto")
                else:
                    print("ERROR17: Imposible acceder a esa posición")
            else:
                print("ERROR18: Vector ", p[1], "no declarada")
        elif '.' in p[1] and len(p)==7:
            names = p[1].split('.')
            name = self.variables[names[0]]
            for a in range(1, len(names)):
                if names[a] in name['valor']:
                    name = name['valor'][names[a]]
                else:
                    print("ERROR19: Variable ", names[a], "no está en el registro", name['tipo'])

            if type(p[3]) == int and p[3] < name['tam']:

                if name['tipo'].upper() == 'ENTERO' and type(p[6]) == int or name[
                    'tipo'].upper() == 'REAL' and type(p[6]) == float \
                        or name['tipo'].upper() == 'BOOLEANO' and type(p[6]) == bool or \
                        name['tipo'].upper() == 'CARACTER' and type(
                    p[6]) == str:
                    name['valor'][p[3]] = p[6]
                elif name['tipo'].upper() == 'ENTERO' and type(p[6]) == str:
                    name['valor'][p[3]] = ord(p[6])

                elif name['tipo'].upper() == 'REAL' and type(p[6]) == int:
                    name['valor'][p[3]] = float(p[6])

                else:
                    print("ERROR20: Tipo incorrecto")




    def p_def_funcion(self, p):
        '''def_funcion : FUNCION NAME '(' lista_args ')' ':' tipo  '{' FINPARRAFO statements1 DEVOLVER expresion  '}'  '''
        # Agrega la acción semántica aquí


    def p_lista_args(self, p):
        '''lista_args : tipo NAME ',' lista_args
                      | tipo NAME
                      |'''
        #lista de argumentos que declaramos cuando declaramos una función
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 4:
            if p[3]:
                p[0] = p[1] + ',' + p[3]
            else:
                p[0] = p[1]

        print("p_lista_args", p[0])


    def p_expresion(self, p):
        '''expresion : expresion_and OR expresion
                     | expresion_and '|' expresion
                     | expresion_and'''
        if len(p) == 4:
            p[0] = p[1] or p[3]
        else:
            p[0] = p[1]
        print("p_expresion_or", p[0])

    def p_expresion_and(self, p):
        '''expresion_and : expresion_comp AND expresion_and
                         | expresion_comp '&' expresion_and
                         | expresion_comp'''
        if len(p) == 4:
            p[0] = p[1] and p[3]
        else:
            p[0] = p[1]
        print("p_expresion_and", p[0])

    def p_expresion_comp(self, p):
        '''expresion_comp : expresion_add OPCOMPARE expresion_comp
                          | expresion_add'''

        if len(p) == 4:
            if p[2] == '==':
                p[0] = p[1] == p[3]
            elif p[2] == '<=':
                p[0] = p[1] <= p[3]
            elif p[2] == '>=':
                p[0] = p[1] >= p[3]
            elif p[2] == '<':
                p[0] = p[1] < p[3]
            elif p[2] == '>':
                p[0] = p[1] > p[3]
        else:
            p[0] = p[1]
        print("p_expresion_comp", p[0])

    def p_expresion_add(self, p):
        '''expresion_add : expresion_mult '+' expresion_add
                         | expresion_mult '-' expresion_add
                         | expresion_mult'''
        if len(p) == 4:
            if p[2] == '+':
                p[0] = p[1] + p[3]
            elif p[2] == '-':
                p[0] = p[1] - p[3]
        else:
            p[0] = p[1]
        print("p_expresion_add", p[0])

    def p_expresion_mult(self, p):
        '''expresion_mult : factor '*' expresion_mult
                          | factor '/' expresion_mult
                          | factor'''

        if len(p) == 4:
            if p[2] == '*':
                p[0] = p[1] * p[3]
            elif p[2] == '/':
                p[0] = p[1] / p[3]
        else:
            p[0] = p[1]
        print("p_expresion_mult", p[0])

    def p_factor(self, p):
        '''factor : '(' expresion ')'
                  | valor
                  | NAME '(' lista_expresiones ')'
                  | operador_unario factor
                  '''

        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 3:
            #¿comprobar aqui que factor no sea unn caracter?, podría hacerse para recuperarse de errores
            if p[1] == '+':
                p[0] = p[2]
            elif p[1] == '-':
                p[0] = - p[2]
            elif p[1] == '!' or p[1] == 'NOT':
                p[0] = not(p[2])
        elif len(p) == 4:
            p[0] = p[2]
        elif len(p) == 5:
            # para el caso de name_chain '(' lista_expresiones ')', es cuando se usa una función ver como guardar las acciones de funcion y como usarlos
            #también como comprobar los tipos
            pass

        print("p_factor", p[0])
        # Agrega la acción semántica aquí
    def p_lista_expresiones(self, p):
        '''lista_expresiones : expresion ',' lista_expresiones
                             | expresion
                             |'''
        # Esto es para parar una lista de expresiones a una función
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 4:
            if p[3]:
                p[0] = p[1] + ',' + p[3]
            else:
                p[0] = p[1]


        print("p_lista_expresiones", p[0])


    def p_operador_unario(self, p):
        '''operador_unario : '-'
                           | NOT
                           | '!'
                           | '+'
                           '''
        p[0] = p[1]
        print("p_operador_unario", p[0])
        # Agrega la acción semántica aquí

    def p_valor(self, p):
        '''valor : NUMREAL
                 | NUMINTEGER
                 | CIERTO
                 | FALSO
                 | CARACTERC
                 | name_chain
                 | name_chain '.' LONG '''
        #siempre devolverá un número o un boolean o un caracter, numca un name

        if len(p) == 2:
            if type(p[1]) == str and p[1].upper() == 'CIERTO':
                p[0] = True
            elif type(p[1]) == str and p[1].upper() == 'FALSO':
                p[0] = False
            elif isinstance(p[1], str):
                # puede ser caracterc o name_chain
                if len(p[1]) == 1:
                    p[0] = p[1]
                else:
                    if '.' in p[1]:
                        names = p[1].split('.')
                        name = self.variables[names[0]]
                        for a in range(1, len(names)):
                            if names[a] in name['valor']:
                                name = name['valor'][names[a]]
                            else:
                                print("ERROR21: Variable ", names[a], "no está en el registro", name['tipo'])
                        p[0] = name['valor']
                    else:

                        if p[1] in self.variables:
                            p[0] = self.variables[p[1]]['valor']
                        else:
                            print("ERROR22: Variable ", p[1], "no declarada")

                 
            # no se diferencia entre int o float, podríamos volver a juntarlos en el lex
            elif isinstance(p[1], int):
                p[0] = p[1]
            elif isinstance(p[1], float):
                p[0] = p[1]


        elif len(p) == 4:
            #name_chain '.' LONG; tamaño del vector, buscar la biblioteca de vectores y obtener su tamaño
            pass


        print("p_valor", p[0])

    def p_condicional(self, p):
        '''condicional : SI expresion FINPARRAFO ENTONCES FINPARRAFO statements1 SINO FINPARRAFO statements1  FINSI
                    | SI expresion FINPARRAFO ENTONCES FINPARRAFO statements1 FINSI'''
        # Agrega la acción semántica aquí


    def p_bucle(self, p):
        '''bucle : MIENTRAS expresion statements1 FINMIENTRAS
        '''
        # Agrega la acción semántica aquí

    def p_name_chain(self, p):
        '''name_chain : NAME
                    | name_chain '.' NAME'''

        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 4:
            p[0] = p[1] + '.' + p[3]

        print("p_name_chain", p[0])



    def p_error(self, p):
        if p:
            print("Syntax error at '%s'" % p.value)
        else:
            print("Syntax error at EOF")

    def check_and_assign_variable(self, tipo, name, valor, registro=False):
        if name not in self.names:
            if registro or (tipo == 'ENTERO' and isinstance(valor, int)) or (
                    tipo == 'REAL' and isinstance(valor, float)) \
                    or (tipo == 'BOOLEANO' and isinstance(valor, bool)) or (
                    tipo == 'CARACTER' and isinstance(valor, str)):
                self.variables[name] = {'tipo': tipo, 'valor': valor}
                self.names.append(name)
            elif tipo == 'ENTERO' and isinstance(valor, str):
                self.variables[name] = {'tipo': tipo, 'valor': ord(valor)}
                self.names.append(name)
            elif tipo == 'REAL' and isinstance(valor, int):
                self.variables[name] = {'tipo': tipo, 'valor': float(valor)}
                self.names.append(name)
            else:
                print("ERROR: Tipo incorrecto ")
        else:
            print("ERROR: Variable ", name, "ya declarada")

    def assign_values(self, tipo, names, valor, dic=None):
        nombres = {}
        for name in names.split(','):
            nombres[name] = {'tipo': tipo, 'valor': valor}
        if dic:
            dic.update(nombres)
            return dic
        else:
            return nombres

