import pyomo.environ as pyo
# Ejemplo del problema de transporte de las cervezas utilizando Pyomo
# Creamos el modelo
modelo = pyo.ConcreteModel()

# Creamos los nodos de oferta y demanda
modelo.i = pyo.Set(initialize=['Cervecería A','Cervecería B'], doc='Cervecerías')
modelo.j = pyo.Set(initialize=['Bar 1', 'Bar 2', 'Bar 3', 'Bar 4', 'Bar 5'],
               doc='Bares')

# Definimos las capacidades de oferta y demanda
modelo.a = pyo.Param(modelo.i, initialize={'Cervecería A':1000,'Cervecería B':4000},
                 doc='Capacidad de oferta de las cervecerías')
modelo.b = pyo.Param(modelo.j, initialize={'Bar 1':500,'Bar 2':900,'Bar 3':1800, 
                                      'Bar 4':200, 'Bar 5':700 },
                 doc='Demanda de cada bar')

# Costo de transporte
costos = {
    ('Cervecería A', 'Bar 1'): 2,
    ('Cervecería A', 'Bar 2'): 4,
    ('Cervecería A', 'Bar 3'): 5,
    ('Cervecería A', 'Bar 4'): 2,
    ('Cervecería A', 'Bar 5'): 1,
    ('Cervecería B', 'Bar 1'): 3,
    ('Cervecería B', 'Bar 2'): 1,
    ('Cervecería B', 'Bar 3'): 3,
    ('Cervecería B', 'Bar 4'): 2,
    ('Cervecería B', 'Bar 5'): 3
    }

modelo.d = pyo.Param(modelo.i, modelo.j, initialize=costos, 
                doc='Costo de transporte')


# definimos el costo de tranporte
def f_costo(modelo, i, j):
    return modelo.d[i,j]

modelo.c = pyo.Param(modelo.i, modelo.j, initialize=f_costo, 
                doc='Costo de transporte')

# definimos variable x con las cantidades de cajas enviadas
modelo.x = pyo.Var(modelo.i, modelo.j, bounds=(0.0,None), 
              doc='Cantidad de cajas')

## Definimos las restricciones ##
# Límite de oferta
def f_oferta(modelo, i):
    return sum(modelo.x[i,j] for j in modelo.j) <= modelo.a[i]
modelo.oferta = pyo.Constraint(modelo.i, rule=f_oferta, 
                           doc='Límites oferta de cada Cervecería')

# Límite de demanda
def f_demanda(modelo, j):
    return sum(modelo.x[i,j] for i in modelo.i) >= modelo.b[j]  
modelo.demanda = pyo.Constraint(modelo.j, rule=f_demanda, 
                            doc='Límites demanda de cada bar')

## Definimos la función objetivo y resolvemos el problema ##
# Función objetivo
def f_objetivo(modelo):
    return sum(modelo.c[i,j]*modelo.x[i,j] for i in modelo.i for j in modelo.j)
modelo.objetivo = pyo.Objective(rule=f_objetivo, sense=pyo.minimize, 
                           doc='Función Objetivo')

# resolvemos el problema e imprimimos resultados
def pyomo_postprocess(options=None, instance=None, results=None):
    modelo.x.display()

# utilizamos solver glpk
opt = pyo.SolverFactory("glpk")

resultados = opt.solve(modelo)

# imprimimos resultados
print("\nSolución óptima encontrada\n" + '-'*80)
pyomo_postprocess(None, None, resultados)