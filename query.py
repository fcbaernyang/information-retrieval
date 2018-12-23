# coding = utf-8

from word2vec import load_model
from utils import *
from data_helpers import preprocess

def gene_split(gene_field):
    '''
    基因字段有特殊格式

    Args:
        gene_field str 基因字段
    Returns:
        gene_list list 切分后的gene字段
    '''
    pass

def demographic_split(demographic_field):
    '''
    人口信息字段有特殊格式

    Args:
        demographic_field str demographic字段
    Returns:
        demographic_list list 切分后的demographic字段
    '''
    # 人口信息有特殊格式
    demographic_list = demographic_field.split(' ')
    age = demographic_list[0]
    age_list = age.split('-')
    sex = demographic_list[1]
    demographic_list = []
    demographic_list.extend(age_list)
    demographic_list.append(sex)
    return demographic_list

def query_extension(field_list, query_dict, w2v_model, vocab, k):
    '''
    查询扩展
    
    Args:
        field_list list 相应字段的列表
        query_dict dict 扩展前的查询字典（键为查询词，值为相近词）
        w2v_model bin 词向量模型
        vocab list 词典
        k int 前k个相近词
    Returns:
        query_dict dict 扩展后的查询字典（键为查询词，值为相近词）
    '''
    for query in field_list:
        if query not in vocab:
            continue
        sim_word_list = w2v_model.wv.most_similar_cosmul(query, topn = k)
        for word, _ in sim_word_list:
            if query in query_dict.keys():
                query_dict[query].append(word)
            else:
                query_dict[query] = [word]
    return query_dict

def build_query(data_path, w2v_path, vocab_path, k):
    '''
    构建查询
    
    Args:
        data_path str 查询文件路径
        model_path str 词向量模型路径
        vocab_path str 词典路径
        k int 返回前k个相近词
    Returns:
        query_list list 已扩展的查询列表
    '''
    # 载入词向量模型，词典模型
    w2v_model = load_model(w2v_path)
    vocab = pickle_load(vocab_path)
    query_list = []
    # 解析xml文档
    query_dict = xml_parse(data_path)
    disease_field_list = query_dict['disease']
    gene_field_list = query_dict['gene']
    demographic_field_list = query_dict['demographic']
    other_field_list = query_dict['other']
    # 遍历查询
    for i in range(len(disease_field_list)):
        query_tmp_dict = {}
        # 获取一条查询的查询词
        disease_field_list[i] = preprocess(disease_field_list[i])
        disease_list = disease_field_list[i].split(' ')
        gene_field_list[i] = preprocess(gene_field_list[i])
        gene_list = gene_field_list[i].split(' ')
        other_list = preprocess(other_field_list[i])
        other_list = other_field_list[i].split(' ')
        demographic_list = demographic_split(demographic_field_list[i])     
        # 查询扩展
        query_tmp_dict = query_extension(disease_list, query_tmp_dict, w2v_model, vocab, k)
        query_tmp_dict = query_extension(gene_list, query_tmp_dict, w2v_model, vocab, k)
        query_tmp_dict = query_extension(demographic_list, query_tmp_dict, w2v_model, vocab, k)
        query_tmp_dict = query_extension(other_list, query_tmp_dict, w2v_model, vocab, k)
        query_list.append(query_tmp_dict)
    return query_list