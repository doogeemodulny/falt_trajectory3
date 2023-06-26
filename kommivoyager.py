import numpy as np
import logging
"""
Было использовано описание алгоритма Литтла из источника: https://habr.com/ru/post/332208/
"""
logging.basicConfig(filename='log.txt', level=logging.INFO)


class LittleSolver:
    """ Класс, реализующий решение задачи Коммивояжёра алгоритмом Литтла

    Attributes
    -------------
    record : double
        длина кратчайшего пути
    path : list
        список номеров вершин, обход которых в порядке того, как они лежат в этом списке, составляет кратчайший путь
    -------------

    Methods
    -------------
    setInf(Matrix)
        Принимает в себя суженную матрицу, и ставит бесконечность в недостающем её месте
    substractFromMatrix(Matrix)
        Выполняет прогонку по строкам и столбцам и высчитывает нижнюю грань
    getCoefficient(Matrix, i, j)
        Высчитывает коэффициент для нуля данной матрицы, лежащего по i,j координате
    pathGenerator(path, begin)
        Принимает список ребёр из пути и превращает его в список вершин, начиная с begin
    getMaxCoeffElement(Matrix)
        Вычисляет нуль матрицы с максимальным коэффициентом
    solve(Matrix, indexMatrix, path=None, bottomLimit=0)
        Выполняет алгоритм Литтла и заполняет поля path (пока списком ребёр) и record
    findPath(matrix, beginValue=0)
        Главный метод, генерирующий матрицу индексов и возвращающий path и record
    -------------
    """
    def __init__(self):
        self.record = np.inf
        self.path = []

    @staticmethod
    def pathLen(matrix, path, end):
        """

        Parameters
        ----------
        matrix : np.array
            Матрица весов графа
        path : np.array
            Путь, длину которого нужно искать
        end : int
            Номер конечной точки, до которой нужно посчитать путь

        Returns
        -------
        res : int
            Длина заданного пути path до точки end
        """
        res = 0
        i = 0
        while path[i] != end:
            res += matrix[path[i]][path[i+1]]
        return res

    @staticmethod
    def setInf(matrix):
        """Принимает в себя суженную матрицу, и ставит бесконечность в недостающем её месте

        Arguments
        matrix : np.array
            Суженная матрица, в которую нужно вставить бесконечность

        Return
        Матрица со вставленной бесконечностью : np.array
        """
        k = 0
        l = 0
        for i in range(matrix.shape[0]):
            flag = 0
            for j in range(matrix.shape[1]):
                if matrix[i][j] == np.inf:
                    flag = 1
            if flag == 0:
                k = i
                break

        for j in range(matrix.shape[1]):
            flag = 0
            for i in range(matrix.shape[0]):
                if matrix[i][j] == np.inf:
                    flag = 1
            if flag == 0:
                l = j
                break

        m = matrix.copy()
        m[k][l] = np.inf
        return m

    @staticmethod
    def substractFromMatrix(Matrix):
        """Выполняет прогонку по строкам и столбцам и высчитывает нижнюю грань

        Arguments
        Matrix : np.array
            Матрица весов

        Return
        subtractSum : int
            Коэффициент прогонки
        m : np.array
            Новая матрица весов
        """
        m = Matrix.copy()
        substractSum = 0

        row_min = np.min(m, 1)
        for i in range(m.shape[1]):
            if row_min[i] != np.inf:
                m[i] -= row_min[i]

        col_min = np.min(m, 0)
        for i in range(m.shape[0]):
            m[:, i] -= col_min[i]

        substractSum += np.sum(col_min)
        substractSum += np.sum(row_min)
        return substractSum, m

    @staticmethod
    def getCoefficient(Matrix, i, j):  #
        """ Высчитывает коэффициент для нуля данной матрицы, лежащего по i,j координате

        Arguments
        Matrix : np.array
            Матрица весов
        i, j : int
            Координаты нуля (i-тая строка, j-тый столбец)

        Return
        Коэффициент нуля : int
        """
        m = Matrix.copy()
        m[i][j] = np.inf

        rmin = np.min(m[i])
        cmin = np.min(m[:, j])

        return rmin + cmin if rmin + cmin != np.inf else 0

    @staticmethod
    def pathGenerator(path, beginValues):
        """Принимает в себя path в виде списка ребёр, и строит из него путь в виде списка вершин, учитывая начальную вершину (begin)

        Arguments
        path : list
            Список ребёр пути
        begin : int
            Начальная вершина

        Return
        Путь, состоящий из списка вершин, начиная с begin : list
        """

        genPaths = []

        for i in beginValues:
            genPath = []
            genPath.append(beginValues[0])
            pastNumber = i
            flag = True

            while pastNumber != i or flag:
                flag = False
                for way in path:
                    if way[0] == pastNumber:
                        nextNumber = way[1]
                        if nextNumber == i:
                            nextNumber = beginValues[0]
                        genPath.append(nextNumber)
                        pastNumber = way[1]
                        break
            genPaths.append(genPath)

        return genPaths

    def getMaxCoeffElement(self, Matrix):
        """Вычисляет коэфф. для каждого нуля, и выбирает нуль с максимальным

        Arguments
        Matrix : np.array
            Исходная матрица

        Return
        Номер строки нуля с максимальным коэффициентом : int
        Номер столбца нуля с максимальным коэффициентом : int
        """
        coeffs = []
        m = np.nonzero(Matrix == 0)
        for i in range(m[0].size):
            coeffs.append(self.getCoefficient(Matrix, m[0][i], m[1][i]))

        coeffs = np.array(coeffs)
        maxCoeff = np.max(coeffs)
        maxNum = np.nonzero(coeffs == maxCoeff)[0][0]

        return m[0][maxNum], m[1][maxNum]

    def solve(self, Matrix, indexMatrix, path=None, bottomLimit=0):
        """ Полностью выполняет алгоритм Литтла

        Arguments
        Matrix : np.array
            Матрица весов графа
        indexMatrix : np.array
            Матрица индексов элементов (нужна, чтобы знать координаты ребёр). Генерируется в findPath
        path : list
            Список уже пройденных ребёр
        bottomLimit : int
            Верхняя граница путей, нужная для отсеивания длинных путей
        """
        if not path:
            path = []

        if Matrix.shape == (2, 2):  # Если осталась матрица размером 2Х2, то это конечный шаг. Проверяем, подходит ли она для кратчайшего пути, и загоняем оставшиеся рёбра в path
            k = np.nonzero(Matrix != np.inf)
            lastSteps = [Matrix[k[0][i]][k[1][i]] for i in range(k[0].size)]
            bottomLimit += np.sum(lastSteps)
            if self.record > bottomLimit:
                self.record = bottomLimit
            path.append(indexMatrix[k[0][0]][k[1][0]])
            if len(k[0]) == 2:
                path.append(indexMatrix[k[0][1]][k[1][1]])
            self.path = path.copy()
            return

        addBottomLimit, newMatrix = self.substractFromMatrix(Matrix)  #  Преобразовываем матрицу, и высчитываем среднюю грань для неё
        bottomLimit += addBottomLimit
        if bottomLimit > self.record:
            return

        i, j = self.getMaxCoeffElement(newMatrix)  # Вычисляем координаты нуля с максимальным коэфф., и добавляем их в новый путь
        newPath = path.copy()
        newPath.append(indexMatrix[i][j])

        M1 = newMatrix.copy()  #  Раздваиваем поиск на две матрицы: Там, где мы добавили ребро в путь, и там где убрали (М1 и М2). Здесь определили М1
        indexM1 = indexMatrix.copy()
        indexM1 = np.delete(indexM1, i, 0)
        indexM1 = np.delete(indexM1, j, 1)
        M1 = np.delete(M1, i, 0)
        M1 = np.delete(M1, j, 1)
        M1 = self.setInf(M1)

        M2 = newMatrix.copy()  # Здесь определили М2
        M2[i][j] = np.Inf

        self.solve(M1, indexM1, newPath, bottomLimit) # Запускаем рекурсию по двум новым путям
        self.solve(M2, indexMatrix, path, bottomLimit)

    def findPath(self, matrix, beginValue = 0, planeCount=1):
        """ Главный метод. Генерирует матрицу индексов, и запускает solve. Возвращает path и record.

        Arguments
        matrix : np.array
            Матрица весов графа
        beginValues : np.array
            Список вершин, с которых начинает обход каждый беспилотник
        planeCount : int
            Количество беспилотников

        Return
        path : list
            Кратчайший путь, являющийся списком вершин
        record : int
            Длина кратчайшего пути
        """
        logging.info('Алгоритм начал работу')

        newMatrix = np.full(shape=(matrix.shape[0]+planeCount - 1, matrix.shape[1]+planeCount - 1), fill_value=np.inf)
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[0]):
                newMatrix[i][j] = matrix[i][j]
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[0], newMatrix.shape[0]):
                if matrix[i][beginValue] != np.inf:
                    newMatrix[i][j] = matrix[i][beginValue]
        for i in range(matrix.shape[0], newMatrix.shape[0]):
            for j in range(matrix.shape[0]):
                newMatrix[i][j] = matrix[beginValue][j]
        self.record = np.inf
        self.path = []
        indexMatrix = np.array([[[i, j] for j in range(newMatrix.shape[0])] for i in range(newMatrix.shape[1])])
        self.solve(newMatrix, indexMatrix)
        beginValues = [i for i in range(matrix.shape[0], matrix.shape[0] + planeCount - 1)]
        beginValues.insert(0, beginValue)
        self.path = self.pathGenerator(self.path, beginValues)

        #for i in range(matrix.shape[0]):
            #if i in points:
                #continue
           # min_path = np.inf
            #for j in range(planeCount):
              #  if self.pathLen(matrix, paths[j], i):
        logging.info('Алгоритм успешно завершился')
        return self.path, self.record



