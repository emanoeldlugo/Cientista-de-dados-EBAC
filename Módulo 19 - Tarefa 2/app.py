import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image
import timeit
from io import BytesIO

custom_params = {'axes.spines.right': False, 'axes.spines.top': False}
sns.set_theme(style='ticks', rc=custom_params)

@st.cache_data
def df_to_string(df):
    return df.to_csv(sep=';', index=False)


@st.cache_data
def df_to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.close()    
    proecessed_data = output.getvalue()
    return proecessed_data

@st.cache_data
def load_data(file_data):
    try:
        return pd.read_csv(file_data, sep=';')
    except:
        return pd.read_excel(file_data)

@st.cache_data
def multiselect_filter(relatorio, col, selecionados):
    if 'all' in selecionados:
        return relatorio
    else:
        return relatorio[relatorio[col].isin(selecionados)].reset_index(drop=True)

def main():
    st.set_page_config(page_title='Análise de Telemarketing',
                       page_icon= 'venv/img/logo.png',
                       layout='wide',
                       initial_sidebar_state='expanded')
    
    st.title('Análise de Telemarketing')
    st.markdown('---')

    image = Image.open('venv/img/fundo.png')
    st.sidebar.image(image)

    bank_raw = load_data('./bank-additional-full.csv')

    bank = bank_raw.copy()

    st.sidebar.write('## Suba o arquivo')
    data_file_1 = st.sidebar.file_uploader("Bank marketing data", type=['csv', 'xlsx'])

    if (data_file_1 is not None):
        start = timeit.default_timer()
        bank_raw = load_data(data_file_1)

        st.write(f'Time: {timeit.default_timer() - start:.10f}')
        bank = bank_raw.copy()
        st.write(bank_raw.head())

    st.sidebar.write(data_file_1)


    st.write('## Antes dos filtros')
    st.write(bank_raw.head())

    # csv = df_to_string(bank_raw)
    # st.write(type(csv))
    # st.write(csv[:100])

    # st.write('### Download CSV')

    # st.download_button(label='Download CSV',
    #                    data=csv,
    #                    file_name='bank_csv_download.csv',
    #                    mime='text/csv')

    df_xlsx = df_to_excel(bank_raw)
    #st.write(type(df_xlsx))
    #st.write(df_xlsx[:100])

    st.write('### Download Excel')

    st.download_button(label='Download data as EXCEL',
                       data=df_xlsx,
                       file_name='bank_xlsx_download.xlsx')
    
    

    with st.sidebar.form(key='my_form'):

        # Selecionar o tipo de gráfico
        graph_type = st.radio('Tipo de gráfico', ('Barra', 'Pizza'))

        # Idades
        max_age = int(bank['age'].max())
        min_age = int(bank['age'].min())
        idade = st.slider(label = 'Idade', 
                              min_value = min_age, 
                              max_value = max_age, 
                              value = (min_age, max_age),
                              step=1)
        st.write(f'Idade selecionada: {idade[0]} - {idade[1]}')
        st.write(f'Menor idade: {idade[0]}')
        st.write(f'Maior idade: {idade[1]}')

        bank = bank[(bank['age'] >= idade[0]) & (bank['age'] <= idade[1])]

        # Profissões

        jobs_list = bank['job'].unique().tolist()
        jobs_list.append('all')
        jobs_selected = st.multiselect('Profissão', jobs_list, ['all'])

        # Estado Civil

        marital_list = bank['marital'].unique().tolist()
        marital_list.append('all')
        marital_selected = st.multiselect('Estado civil', marital_list, ['all'])

        
        # Default

        default_list = bank['default'].unique().tolist()
        default_list.append('all')
        default_selected = st.multiselect('Default', default_list, ['all'])

        # Housing

        housing_list = bank['housing'].unique().tolist()
        housing_list.append('all')
        housing_selected = st.multiselect('Tem finan. imob.?', housing_list, ['all'])        

        # Loan

        loan_list = bank['loan'].unique().tolist()
        loan_list.append('all')
        loan_selected = st.multiselect('Tem empréstimo?', loan_list, ['all'])     

        # Contact

        contact_list = bank['contact'].unique().tolist()
        contact_list.append('all')
        contact_selected = st.multiselect('Meio de Contato', contact_list, ['all'])            

        # Mês de contato

        month_list = bank['month'].unique().tolist()
        month_list.append('all')
        month_selected = st.multiselect('Mês do contato', month_list, ['all'])

        # Dia da semana

        day_of_week_list = bank['day_of_week'].unique().tolist()
        day_of_week_list.append('all')
        day_of_week_selected = st.multiselect('Dia da semana', day_of_week_list, ['all'])


        bank = (bank.query('age >= @idade[0] and age <= @idade[1]')
                .pipe(multiselect_filter, 'job', jobs_selected)
                .pipe(multiselect_filter, 'marital', marital_selected)	
                .pipe(multiselect_filter, 'default', default_selected)
                .pipe(multiselect_filter, 'housing', housing_selected)
                .pipe(multiselect_filter, 'loan', loan_selected)
                .pipe(multiselect_filter, 'contact', contact_selected)
                .pipe(multiselect_filter, 'month', month_selected)
                .pipe(multiselect_filter, 'day_of_week', day_of_week_selected))

        #bank = bank[(bank['age'] >= idade[0]) & (bank['age'] <= idade[1])]
        #bank = multiselect_filter(bank, 'job', jobs_selected)

        submit_button = st.form_submit_button(label='Aplicar')

    st.write('## Após os filtros')
    st.write(bank.head())
    st.markdown('---')

    col1_target, col2_target = st.columns(2)

    with col1_target:
        bank_raw_target_perc = bank_raw['y'].value_counts(normalize = True).to_frame()*100
        bank_raw_target_perc = bank_raw_target_perc.sort_index().reset_index()
        bank_raw_target_perc
        bank_raw_target_perc_xlsx = df_to_excel(bank_raw_target_perc)
        st.write('### Download Excel')
        st.download_button(label='Download data as EXCEL',
                        data=bank_raw_target_perc_xlsx,
                        file_name='bank_raw_target_perc_xlsx_download.xlsx')

    with col2_target:
        bank_target_perc = bank['y'].value_counts(normalize = True).to_frame()*100
        bank_target_perc = bank_target_perc.sort_index().reset_index()
        bank_target_perc
        bank_target_perc_xlsx = df_to_excel(bank_target_perc)
        st.write('### Download Excel')
        st.download_button(label='Download data as EXCEL',
                        data=bank_target_perc_xlsx,
                        file_name='bank_target_perc_xlsx_download.xlsx')


    st.write("bank_raw_target_perc columns:", bank_raw_target_perc.columns.tolist())
    st.write(bank_raw_target_perc)


    # # PLOTS
    fig, ax = plt.subplots(1, 2, figsize=(8, 4))  # aumentei um pouco o tamanho para melhor visualização

    st.write('## Proporção de aceite')

    col1, col2, col3 = st.columns([1, 2, 1])  # centraliza o gráfico no meio

    with col2:
        if graph_type == 'Barra':
            sns.barplot(x='y', y='proportion', data=bank_raw_target_perc, ax=ax[0])
            ax[0].bar_label(ax[0].containers[0])
            ax[0].set_title('Dados brutos', fontweight="bold")
            ax[0].set_ylim(0, 100)

            sns.barplot(x='y', y='proportion', data=bank_target_perc, ax=ax[1])
            ax[1].bar_label(ax[1].containers[0])
            ax[1].set_title('Dados filtrados', fontweight="bold")
            ax[1].set_ylim(0, 100)

            for i in [0, 1]:
                for side in ['top', 'right', 'left']:
                    ax[i].spines[side].set_visible(False)
                ax[i].tick_params(left=False, labelleft=False)
                ax[i].set_ylabel('')
                ax[i].set_xlabel('')
        
        else:  # gráfico de pizza
            bank_raw_target_perc.set_index('y')['proportion'].plot.pie(
                autopct='%.2f%%', ax=ax[0], legend=False, ylabel='')
            ax[0].set_title('Dados brutos', fontweight="bold")

            bank_target_perc.set_index('y')['proportion'].plot.pie(
                autopct='%.2f%%', ax=ax[1], legend=False, ylabel='')
            ax[1].set_title('Dados filtrados', fontweight="bold")

        st.pyplot(fig)  # passa a figura ao invés de plt (recomendado)




if __name__ == '__main__':
    main()
