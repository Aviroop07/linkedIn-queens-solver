import streamlit as st

def main():
    st.write('''
    ## 🔄 About This App 🔄
    ''')
    st.markdown('''
    ##### This application is designed to solve the Queens game, a visual logic game from LinkedIn News where you need to fill the grid so that there is one Queen (👑) in each row, column, and colored region with no 👑 touching another (even diagonally). Give it a play at https://www.linkedin.com/games/queens/. New editions drop daily.
    ''')

    
    st.write('')
    st.write('''
    ## 👨‍💻 About the developer 👨‍💻
    ''')
    st.markdown('''
    ##### This application was developed by [Aviroop Mitra](https://www.linkedin.com/in/aviroopmitra071003/)
    ''')

    st.write('')
    st.write('''
    ## 🚨 Disclaimer 🚨
    ##### This application is purely a personal project and is not intended for any commercial purposes.
    ''')

if __name__ == "__main__":
    main()
