import help
import math
OR_QUERY = 0
AND_QUERY = 1
PHARSE_QUERY = 2


class InformationFind:
    # filenames = []		# список файлов
    # inverted_index = {}	# обратный индекс
    # document_vector = {}	# вектор для ранжирования
    # files_size = []		# список длин файлов
    # word_count = []		# кол-во слов во всех файлах
    
    
    # public
    def __init__(self, filenames):		# конструктор от списка файлов
        self.filenames = filenames
        self.process_data()
    
    
    # private
    def process_data(self):				# загрузка данных / построение структур (часть конструктора)
        self.process_files()
        self.get_inverted_index()
        self.get_document_vector()
        self.get_tf_idf()
    
    
    # private
    def process_files(self):			# чтение файлов и подсчет их размеров (часть загрузки данных)
        files_size = []
        files_terms = {}
        for file in self.filenames:
            files_terms[file] = help.split_string(open(file, 'r').read())
            files_size.append(len(files_terms[file]))
        self.inverted_index = files_terms
        self.files_size = files_size
    
    
    # private
    def get_inverted_index(self):		# построение обратного индекса (часть загрузки данных)
        result = {}
        for file in self.inverted_index.keys():
            for position in range(len(self.inverted_index[file])):
                word = self.inverted_index[file][position]
                if word in result.keys():
                    if file in result[word].keys():
                        result[word][file].append(position)
                    else:
                        result[word][file] = [position]
                else:
                    result[word] = {file : [position]}
        self.inverted_index = result
    
    
    # private
    def get_document_vector(self):		# построение вектора и подсчет числа слов во всех файлах (часть загрузки данных)
        self.document_vector = {}
        self.word_count = []
        for file in self.filenames:
            self.document_vector[file] = []
        for word in self.inverted_index.keys():
            this_word_count = 0
            for file in self.filenames:
                if file in self.inverted_index[word].keys():
                    self.document_vector[file].append(len(self.inverted_index[word][file]))
                    this_word_count += self.document_vector[file][-1]
                else:
                    self.document_vector[file].append(0)
            self.word_count.append(this_word_count)
    
    
    # private
    def get_tf_idf(self):				# подсчёт tf-idf для всех файлов (часть загрузки данных)
        for file_position in range(len(self.filenames)):
            file = self.filenames[file_position]
            for word_position in range(len(self.document_vector[file])):
                self.document_vector[file][word_position] = self.tf_idf(self.document_vector[file][word_position], self.files_size[file_position], self.word_count[word_position])
    
    
    # public
    def files_with_text(self, query_string, query_type = OR_QUERY):		# поисковый запрос
        query_string = help.split_string(query_string)
        if query_type == OR_QUERY:
            result = self.query_or(query_string)
        elif query_type == AND_QUERY:
            result = self.query_and(query_string)
        elif query_type == PHARSE_QUERY:
            result = self.query_phare(query_string)
        else:
            raise ValueError('Expected constant')
        return self.rank_documents(query_string, result)
    
    
    # private
    def files_with_one_word(self, word):								# запрос с одним словом (часть поискового запроса)
        if word in self.inverted_index.keys():
            return [_ for _ in self.inverted_index[word].keys()]
        else:
            return []
    
    
    # private
    def query_or(self, query_string):									# запрос ИЛИ (часть поискового запроса)
        result = []
        for word in query_string:
            result += self.files_with_one_word(word)
        return list(set(result))
    
    
    # private
    def query_and(self, query_string):									# запрос И (часть поискового запроса)
        result = []
        for word in query_string:
            result.append(self.files_with_one_word(word))
        return list(set(result[0]).intersection(*result))
    
    
    # private
    def query_phare(self, query_string):								# запрос ФРАЗА (часть поискового запроса)
        result = []
        files = self.query_and(query_string)
        for file in files:
            temp = []
            for word in query_string:
                temp.append(self.inverted_index[word][file][:])
            for i in range(len(temp)):
                for j in range(len(temp[i])):
                    temp[i][j] -= i
            if set(temp[0]).intersection(*temp):
                result.append(file)
        return result
    
    
    # private
    def rank_documents(self, query_string, documents):			# ранжирование документов (часть поискового запроса)
        query_vector = self.get_query_vector(query_string)
        result = []
        for file in documents:
            result.append([file, self.dotProduct(self.document_vector[file], query_vector)])
        result.sort(key=lambda x: -x[1])
        return [x[0] for x in result]
    
    
    # private
    def get_query_vector(self, query_string):					# построение вектора для запроса (часть ранжирования)
        result = []
        position = 0
        for word in self.inverted_index.keys():
            result.append(self.tf_idf(query_string.count(word), len(query_string), self.word_count[position]))
            position += 1
        return result
    
    
    # private
    def dotProduct(self, vector1, vector2):						# скалярное произведение векторов (часть ранжирования)
        result = 0
        for position in range(len(vector1)):
            result += vector1[position] * vector2[position]
        return result
    
    
    # private
    def tf_idf(self, word_in_doc, words_in_doc, word_in_files):	# безопасный подсчёт tf-idf (часть загрузки данных и ранжирования)
        if word_in_doc == 0:
            return 0
        else:
            tf = word_in_doc / words_in_doc
            idf = word_in_files / word_in_doc
            return tf * math.log10(idf)
