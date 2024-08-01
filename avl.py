import streamlit as st
from graphviz import Digraph

# Define the Node class
class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

# Utility function to get the height of the tree
def height(N):
    if N is None:
        return 0
    return N.height

# Utility function to get the maximum of two integers
def max(a, b):
    return a if a > b else b

# Right rotate subtree rooted with y
def rightRotate(y):
    x = y.left
    T2 = x.right
    x.right = y
    y.left = T2
    y.height = max(height(y.left), height(y.right)) + 1
    x.height = max(height(x.left), height(x.right)) + 1
    return x, "Right Rotation"

# Left rotate subtree rooted with x
def leftRotate(x):
    y = x.right
    T2 = y.left
    y.left = x
    x.right = T2
    x.height = max(height(x.left), height(x.right)) + 1
    y.height = max(height(y.left), height(y.right)) + 1
    return y, "Left Rotation"

# Left-Right rotate subtree rooted with z
def leftRightRotate(z):
    z.left, _ = leftRotate(z.left)
    return rightRotate(z)[0], "Left-Right Rotation"

# Right-Left rotate subtree rooted with z
def rightLeftRotate(z):
    z.right, _ = rightRotate(z.right)
    return leftRotate(z)[0], "Right-Left Rotation"

# Get the balance factor of node N
def getBalance(N):
    if N is None:
        return 0
    return height(N.left) - height(N.right)

# Recursive function to insert a key in the subtree rooted
# with node and returns the new root of the subtree.
def insert(root, key):
    if not root:
        return Node(key), None
    elif key < root.key:
        root.left, rotation = insert(root.left, key)
    else:
        root.right, rotation = insert(root.right, key)

    root.height = 1 + max(height(root.left), height(root.right))
    balance = getBalance(root)

    # If node becomes unbalanced, then there are 4 cases

    # Left Left Case
    if balance > 1 and key < root.left.key:
        return rightRotate(root)

    # Right Right Case
    if balance < -1 and key > root.right.key:
        return leftRotate(root)

    # Left Right Case
    if balance > 1 and key > root.left.key:
        return leftRightRotate(root)

    # Right Left Case
    if balance < -1 and key < root.right.key:
        return rightLeftRotate(root)

    return root, rotation

# Function to find the node with the minimum key value
# in the tree rooted at node
def minValueNode(node):
    current = node
    while(current.left is not None):
        current = current.left
    return current

# Recursive function to delete a node with given key
# from subtree with given root. It returns root of the
# modified subtree.
def deleteNode(root, key):
    rotation = None  # Initialize rotation variable

    if root is None:
        return root, rotation

    if key < root.key:
        root.left, rotation = deleteNode(root.left, key)
    elif key > root.key:
        root.right, rotation = deleteNode(root.right, key)
    else:
        if root.left is None:
            temp = root.right
            root = None
            return temp, rotation
        elif root.right is None:
            temp = root.left
            root = None
            return temp, rotation

        temp = minValueNode(root.right)
        root.key = temp.key
        root.right, _ = deleteNode(root.right, temp.key)

    if root is None:
        return root, rotation

    root.height = 1 + max(height(root.left), height(root.right))
    balance = getBalance(root)

    # Balance the tree
    # Left Left Case
    if balance > 1 and getBalance(root.left) >= 0:
        return rightRotate(root)

    # Left Right Case
    if balance > 1 and getBalance(root.left) < 0:
        return leftRightRotate(root)

    # Right Right Case
    if balance < -1 and getBalance(root.right) <= 0:
        return leftRotate(root)

    # Right Left Case
    if balance < -1 and getBalance(root.right) > 0:
        return rightLeftRotate(root)

    return root, rotation

# Function to print preorder traversal of the tree
def preOrder(root):
    result = []
    if root:
        result.append(root.key)
        result = result + preOrder(root.left)
        result = result + preOrder(root.right)
    return result

# Function to duplicate the tree
def duplicate_tree(node):
    if node is None:
        return None
    new_node = Node(node.key)
    new_node.left = duplicate_tree(node.left)
    new_node.right = duplicate_tree(node.right)
    new_node.height = node.height
    return new_node

# Function to visualize the tree using graphviz
def visualize_tree(root, graph_name=""):
    def add_nodes_edges(dot, node, parent=None):
        if node is None:
            return
        dot.node(str(node.key), str(node.key))
        if parent:
            dot.edge(str(parent.key), str(node.key))
        add_nodes_edges(dot, node.left, node)
        add_nodes_edges(dot, node.right, node)

    dot = Digraph(name=graph_name)
    add_nodes_edges(dot, root)
    return dot

# Streamlit app
st.title("AVL Tree Implementation")

# Initialize session state to store tree history
if "tree_history" not in st.session_state:
    st.session_state.tree_history = []
if "rotation_info" not in st.session_state:
    st.session_state.rotation_info = []

# Input form
with st.form("AVL Form"):
    option = st.selectbox("Choose an operation", ["Insert", "Delete"])
    key = st.number_input("Enter key", step=1)
    submitted = st.form_submit_button("Submit")

if "avl_tree" not in st.session_state:
    st.session_state.avl_tree = None

rotation_info = None

if submitted:
    old_tree = duplicate_tree(st.session_state.avl_tree)
    if option == "Insert":
        st.session_state.avl_tree, rotation_info = insert(st.session_state.avl_tree, key)
    elif option == "Delete":
        st.session_state.avl_tree, rotation_info = deleteNode(st.session_state.avl_tree, key)

    if rotation_info:
        st.write(f"Rotation performed: {rotation_info}")
        st.session_state.rotation_info.append(f"Tree after {option} {key}: {rotation_info}")
    else:
        st.session_state.rotation_info.append(f"Tree after {option} {key}: No Rotation")
    
    # Store the new tree visualization
    new_tree_visualization = visualize_tree(st.session_state.avl_tree, graph_name=f"Tree after {option} {key}")
    st.session_state.tree_history.append(new_tree_visualization)
    
    # Display previous insertions and the latest tree
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("Previous Trees:")
        for i, (tree, rotation) in enumerate(zip(st.session_state.tree_history, 
                                                 st.session_state.rotation_info)):
            st.write(f"{rotation}")
            st.graphviz_chart(tree)
    
    with col2:
        st.write("Latest Tree:")
        st.graphviz_chart(new_tree_visualization)

st.write("Preorder Traversal of the AVL Tree:")
if st.session_state.avl_tree:
    st.write(preOrder(st.session_state.avl_tree))
else:
    st.write("Tree is empty")
