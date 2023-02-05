from manim import *

class DeepCut(MovingCameraScene):

    def construct(self):
        #####################################################################
        # Logo
        #####################################################################
        circle = Circle()  # create a circle
        circle.set_fill(PINK, opacity=0.5)  # set color and transparency

        square = Square()  # create a square
        square.rotate(PI / 4)  # rotate a certain amount

        self.play(Create(square))  # animate the creation of the square
        self.play(Transform(square, circle))  # interpolate the square into the circle

        deepcut = Text('DeepCut.', color=RED).scale(3)
        self.play(ReplacementTransform(circle,deepcut), FadeOut(square))
        self.play(FadeOut(deepcut))

        
        self.play(self.camera.frame.animate.set(width=20), run_time=0.01)
        #####################################################################
        # image
        #####################################################################        
        
        # Load image
        image = ImageMobject('s.png')
        image.height = 2
        image.to_edge()

        # Image for moving
        image2 = image.copy()
        image.height = 4
        im_tex = Tex("Input \ Image").scale(1).next_to(image,DOWN)

        image2.set_opacity(0.4)

        
        self.play(FadeIn(image))
        self.play(Create(im_tex))
        self.wait(1)
        #####################################################################
        # ViT
        #####################################################################      
        square = Square()
        square.height = 3
        square.set_fill(BLUE, opacity=0.8)
        square.next_to(image, buff=1)
        self.play(Create(square))

        text = Text('ViT').move_to(square.get_center())
        self.add(text)

        self.wait(1)
        # move image into ViT
        self.add(image2)
        self.play(image2.animate.shift(5.20*RIGHT), run_time=2)
        
        #####################################################################
        # embadding vector
        #####################################################################
        
        F = Rectangle(width=4.0, height=0.5, grid_xstep=0.5, grid_ystep=0.5)
        F.next_to(square, buff=1)


        vec_ind = Tex("$x_1 \ x_2 \ x_3 \ x_4 \ x_5 \ x_6 \  ...  \ x_n$", font_size=36).move_to(F.get_center())
        
        F_t = VGroup(F.copy(), vec_ind.copy())
        self.play(Create(F.rotate(PI / 2)))
        self.add(F_t.rotate(-PI / 2))
        self.add(vec_ind.rotate(-PI / 2))
        
        im_tex = Tex("F").scale(1).move_to(np.array((4.4, -2.5, 0.0)))
        im_tex3 = Tex("Deep  \ features  \ vecor").scale(0.75).move_to(np.array((4.4, -3, 0.0)))
        im_vg = VGroup(im_tex, im_tex3)
        self.play(Create(im_vg))
        self.wait(4)

        self.play(F_t.animate.rotate(PI / 2).shift(3*RIGHT))
        im2_tex = Tex("$F * F^T$").scale(1).move_to(np.array((7.0, -2.5, 0.0)))
        self.play(ReplacementTransform(im_vg, im2_tex))
        
        self.play(self.camera.frame.animate.move_to(F_t))
        

        
        #####################################################################
        # Matrix
        #####################################################################
        m2 = Matrix([['x_{1,1}', 'x_{1,2}', '\dotsm', 'x_{1,n}'], ['x_{2,1}', 'x_{2,2}', '\dotsm', 'x_{2,n}'], [ r"\vdots", 'x_{3,2}', '\ddots', 'x_{3,n}'], ['x_{n,1}', 'x_{n,2}', '\dotsm', 'x_{n,n}']])
        m2.next_to(F_t, buff=1)
        self.play(Create(m2),run_time=1.5)
        im_tex = Tex("Correlation \ matrix").scale(1).next_to(m2,DOWN)
        self.play(Create(im_tex))
        self.wait(5)

        self.play(self.camera.frame.animate.move_to(RIGHT * 20))

        #####################################################################
        # Graph
        #####################################################################
        # shift value of clusers Y and X
        Y_1 = 2
        Y_2 = -2
        X_1 = 0.5
        X_2 = -0.5

        # Define graph
        G = Graph([1, 2, 3, 4, 5, 6 ,7 ,8 ,9, 10], [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1), (10,6), (9,7), (9,6), (10,7), (6,7), (10,9), (2,10), (1,9), (1,4), (2,5)],
                  layout={1: [-1 + X_1, -1 + Y_1, 0], 2: [1 + X_1, -1 + Y_1, 0], 3: [0 + X_1, 0 + Y_1, 0], 4: [-1 + X_1, 1 + Y_1, 0], 5: [1 + X_1, 1 + Y_1, 0], 
                          6: [-1 + X_2, -1 + Y_2, 0], 7: [1 + X_2, -1 + Y_2, 0], 8: [0 + X_2, 0 + Y_2, 0], 9: [-1 + X_2, 1 + Y_2, 0], 10: [1 + X_2, 1 + Y_2, 0]},
                labels=True,
                vertex_config={1: {"fill_color": BLUE_E}, 2: {"fill_color": BLUE_E}, 3: {"fill_color": BLUE_E}, 4: {"fill_color": BLUE_E}, 5: {"fill_color": BLUE_E}, 6: {"fill_color": BLUE}, 7: {"fill_color": BLUE}, 8: {"fill_color": BLUE}, 9: {"fill_color": BLUE}, 10: {"fill_color": BLUE}},
                edge_config={(1, 9): {"stroke_color": RED},(2, 10): {"stroke_color": RED}})

        G.next_to(m2, buff=2)
        self.play(Create(G), run_time=2)
        im_tex = Tex("G(V,E)").scale(1).move_to(G.get_bottom() - np.array((0.5, 0.5, 0.0)))

        
        im_tex5 = Tex("V = Image patches").scale(1).move_to(G.get_bottom() + np.array((5, 4, 0.0)))
        im_tex55 = Tex("E = Correlation between patches").scale(1).move_to(G.get_bottom() + np.array((5, 3, 0.0)))
        
        graph_tex = VGroup(im_tex5,im_tex55, im_tex)

        self.play(Create(graph_tex))
        self.wait(10)
        G.remove_edges((1,9),(2,10))
        im2_tex = Tex("Clustered \ graph").scale(1).move_to(G.get_bottom() - np.array((0.5, 0.5, 0.0)))
        self.play(ReplacementTransform(graph_tex, im2_tex))
        self.wait(7)

        #####################################################################
        # Load Mask
        #####################################################################
        image_m = ImageMobject('s_m.png')
        image_m.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
        image_m.height = 4
        image_m.next_to(G, buff=1.5)
        image_m.set_opacity(0)
        # self.add(image_m)
        self.play(image_m.animate.set_opacity(1))
        im_tex = Tex("Output \ mask").scale(1).next_to(image_m,DOWN)
        self.play(Create(im_tex))
        self.wait(3)

        self.play(self.camera.frame.animate.move_to(np.array((10.0, 0.0, 0.0))).set(width=39))
        self.wait()