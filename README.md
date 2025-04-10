# Graphics Engine:
This is a simple python library using pygame-ce to render 3d models, using triangle meshes. Below is an explanation of its different components.

### Point
  Points are a simple class that holds and x,y and z co-ordinates. It exists purely to make code more explicit.
### Triangle
  Triangles are composed of three points, rotational values, and a colour. The rotational values currently have no effect, and will allow compatibility with a later planned project. They also impliment a method that returns their average z co-ordinate, to determine in which order they should be drawn. The co-ordinates of its points are in relation to the object which it will be part of.
### Object
  Objects are composed of a list of triangles, x,y and z co-ordinates and rotational values. They are used to group triangles into more convinient models.
### Renderer
  This class is used to pull everything together. It takes a list of objects, the screen width and height, an object to be treated as the viewpoint, and a focal length. It impliments a method called frame, which returns a pygame surface of the current scene.
