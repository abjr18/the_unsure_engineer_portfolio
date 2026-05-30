import streamlit as st

# Define your pages

create_post_page = st.Page("create_post.py", title="Create a Post", icon="📝")
viewpage = st.Page(page="view_posts.py",title='View Posts')


# Initialize navigation
pg = st.navigation([create_post_page,viewpage])
pg.run()