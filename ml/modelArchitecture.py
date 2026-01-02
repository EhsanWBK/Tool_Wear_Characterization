import keras

class UNet:
    ''' ## Inspiration for the UNet-Model
    Author: Dr. Sreenivas Bhattiprolu (https://youtu.be/csFGTLT6_WQ).'''
    
    def __init__(self) -> None: pass

    def unet_first_iteration(inputShape, n_classes=1):
        '''U-Net Model of first iteration of model training as performed in the Bachelor thesis "Image Processing Based Cutting Tool Monitoring  Using Machine Learning in an Industrial Environment" by Fabian Kohnle. Input:
        - img_shape = (IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS)
        - n_classes (1: binary, ...) '''
        input = keras.Input(inputShape); imgShape = input # First Input Layer

        # Encoder Path
        # First Convolution Layer
        c1 = keras.layers.Conv2D(16, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(imgShape)
        c1 = keras.layers.Dropout(0.1)(c1)
        c1 = keras.layers.Conv2D(16, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c1)
        p1 = keras.layers.MaxPooling2D((2, 2))(c1)
        # Second Convolution Layer
        c2 = keras.layers.Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(p1)
        c2 = keras.layers.Dropout(0.1)(c2)
        c2 = keras.layers.Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c2)
        p2 = keras.layers.MaxPooling2D((2, 2))(c2)
        # Third Convolution Layer
        c3 = keras.layers.Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(p2)
        c3 = keras.layers.Dropout(0.2)(c3)
        c3 = keras.layers.Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c3)
        p3 = keras.layers.MaxPooling2D((2, 2))(c3)
        # Fourth Convolution Layer
        c4 = keras.layers.Conv2D(128, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(p3)
        c4 = keras.layers.Dropout(0.2)(c4)
        c4 = keras.layers.Conv2D(128, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c4)
        p4 = keras.layers.MaxPooling2D(pool_size=(2, 2))(c4)
        # Fifth Convolution Layer
        c5 = keras.layers.Conv2D(256, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(p4)
        c5 = keras.layers.Dropout(0.3)(c5)
        c5 = keras.layers.Conv2D(256, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c5)
        # Decoder Path
        # Sixth Layer: Convolutional Transpose
        u6 = keras.layers.Conv2DTranspose(128, (2, 2), strides=(2, 2), padding='same')(c5)
        u6 = keras.layers.concatenate([u6, c4])
        c6 = keras.layers.Conv2D(128, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(u6)
        c6 = keras.layers.Dropout(0.2)(c6)
        c6 = keras.layers.Conv2D(128, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c6)
        # Seventh Layer: Convolutional Transpose
        u7 = keras.layers.Conv2DTranspose(64, (2, 2), strides=(2, 2), padding='same')(c6)
        u7 = keras.layers.concatenate([u7, c3])
        c7 = keras.layers.Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(u7)
        c7 = keras.layers.Dropout(0.2)(c7)
        c7 = keras.layers.Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c7)
        # Eight Layer: Convolutional Transpose
        u8 = keras.layers.Conv2DTranspose(32, (2, 2), strides=(2, 2), padding='same')(c7)
        u8 = keras.layers.concatenate([u8, c2])
        c8 = keras.layers.Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(u8)
        c8 = keras.layers.Dropout(0.1)(c8)
        c8 = keras.layers.Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c8)
        # Nineth Layer: Convolutional Transpose
        u9 = keras.layers.Conv2DTranspose(16, (2, 2), strides=(2, 2), padding='same')(c8)
        u9 = keras.layers.concatenate([u9, c1], axis=3)
        c9 = keras.layers.Conv2D(16, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(u9)
        c9 = keras.layers.Dropout(0.1)(c9)
        c9 = keras.layers.Conv2D(16, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c9)
        # Output Layer
        outputs = keras.layers.Conv2D(filters=n_classes, kernel_size=1, padding="same", activation = "softmax")(c9)
        model = keras.Model(inputs=[input], outputs=[outputs])
        model.compile(
            optimizer='adam',
            loss=keras.losses.CategoricalCrossentropy(),
            metrics=[keras.metrics.CategoricalAccuracy(),
                    keras.metrics.OneHotIoU(num_classes=n_classes,target_class_ids=range(0,n_classes))])
        return model

    def unet_ehsan(inputShape):
        ''' Differnce to model of first iteration:
        - different call of loss function
        - different call of metrics '''
        inputs = keras.layers.Input(inputShape); s = inputs

        # Encoder Path
        # First Convolution Layer
        c1 = keras.layers.Conv2D(16, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(s)
        c1 = keras.layers.Dropout(0.1)(c1)
        c1 = keras.layers.Conv2D(16, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c1)
        p1 = keras.layers.MaxPooling2D((2, 2))(c1)
        # Second Convolution Layer
        c2 = keras.layers.Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(p1)
        c2 = keras.layers.Dropout(0.1)(c2)
        c2 = keras.layers.Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c2)
        p2 = keras.layers.MaxPooling2D((2, 2))(c2)
        # Third Convolution Layer
        c3 = keras.layers.Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(p2)
        c3 = keras.layers.Dropout(0.2)(c3)
        c3 = keras.layers.Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c3)
        p3 = keras.layers.MaxPooling2D((2, 2))(c3)
        # Fourth Convolution Layer
        c4 = keras.layers.Conv2D(128, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(p3)
        c4 = keras.layers.Dropout(0.2)(c4)
        c4 = keras.layers.Conv2D(128, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c4)
        p4 = keras.layers.MaxPooling2D(pool_size=(2, 2))(c4)
        # Fifth Convolution Layer
        c5 = keras.layers.Conv2D(256, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(p4)
        c5 = keras.layers.Dropout(0.3)(c5)
        c5 = keras.layers.Conv2D(256, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c5)
        # Decoder Path
        # Sixth Layer: Convolutional Transpose
        u6 = keras.layers.Conv2DTranspose(128, (2, 2), strides=(2, 2), padding='same')(c5)
        u6 = keras.layers.concatenate([u6, c4])
        c6 = keras.layers.Conv2D(128, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(u6)
        c6 = keras.layers.Dropout(0.2)(c6)
        c6 = keras.layers.Conv2D(128, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c6)
        # Seventh Layer: Convolutional Transpose
        u7 = keras.layers.Conv2DTranspose(64, (2, 2), strides=(2, 2), padding='same')(c6)
        u7 = keras.layers.concatenate([u7, c3])
        c7 = keras.layers.Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(u7)
        c7 = keras.layers.Dropout(0.2)(c7)
        c7 = keras.layers.Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c7)
        # Eighth Layer: Convolutional Transpose
        u8 = keras.layers.Conv2DTranspose(32, (2, 2), strides=(2, 2), padding='same')(c7)
        u8 = keras.layers.concatenate([u8, c2])
        c8 = keras.layers.Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(u8)
        c8 = keras.layers.Dropout(0.1)(c8)
        c8 = keras.layers.Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c8)
        # Nineth Layer: Convolutional Transpose
        u9 = keras.layers.Conv2DTranspose(16, (2, 2), strides=(2, 2), padding='same')(c8)
        u9 = keras.layers.concatenate([u9, c1], axis=3)
        c9 = keras.layers.Conv2D(16, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(u9)
        c9 = keras.layers.Dropout(0.1)(c9)
        c9 = keras.layers.Conv2D(16, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c9)
        # Outout Layer
        outputs = keras.layers.Conv2D(1, (1, 1), activation='sigmoid')(c9)
        model = keras.Model(inputs=[inputs], outputs=[outputs])
        # model.compile(optimizer='adam', loss='binary_crossentropy', 
        #               metrics=['accuracy', keras.metrics.BinaryIoU(target_class_ids=[0,1])])
        # model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy', keras.metrics.TruePositives(), keras.metrics.TrueNegatives(), keras.metrics.FalsePositives(), keras.metrics.FalseNegatives()])
        model.summary()
        return model
    
    def unet_seg_class(imgShape):
        inputs = keras.layers.Input(shape=imgShape, name='keras_tensor'); s = inputs

        # Encoder Path
        # First Convolution Layer
        c1 = keras.layers.Conv2D(16, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(s)
        c1 = keras.layers.Dropout(0.1)(c1)
        c1 = keras.layers.Conv2D(16, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c1)
        p1 = keras.layers.MaxPooling2D((2, 2))(c1)
        # Second Convolution Layer
        c2 = keras.layers.Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(p1)
        c2 = keras.layers.Dropout(0.1)(c2)
        c2 = keras.layers.Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c2)
        p2 = keras.layers.MaxPooling2D((2, 2))(c2)
        # Third Convolution Layer
        c3 = keras.layers.Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(p2)
        c3 = keras.layers.Dropout(0.2)(c3)
        c3 = keras.layers.Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c3)
        p3 = keras.layers.MaxPooling2D((2, 2))(c3)
        # Fourth Convolution Layer
        c4 = keras.layers.Conv2D(128, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(p3)
        c4 = keras.layers.Dropout(0.2)(c4)
        c4 = keras.layers.Conv2D(128, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c4)
        p4 = keras.layers.MaxPooling2D(pool_size=(2, 2))(c4)
        # Fifth Convolution Layer
        c5 = keras.layers.Conv2D(256, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(p4)
        c5 = keras.layers.Dropout(0.3)(c5)
        c5 = keras.layers.Conv2D(256, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c5)

        # Decoder Path
        # Sixth Layer: Convolutional Transpose
        u6 = keras.layers.Conv2DTranspose(128, (2, 2), strides=(2, 2), padding='same')(c5)
        u6 = keras.layers.concatenate([u6, c4])
        c6 = keras.layers.Conv2D(128, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(u6)
        c6 = keras.layers.Dropout(0.2)(c6)
        c6 = keras.layers.Conv2D(128, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c6)
        # Seventh Layer: Convolutional Transpose
        u7 = keras.layers.Conv2DTranspose(64, (2, 2), strides=(2, 2), padding='same')(c6)
        u7 = keras.layers.concatenate([u7, c3])
        c7 = keras.layers.Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(u7)
        c7 = keras.layers.Dropout(0.2)(c7)
        c7 = keras.layers.Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c7)
        # Eighth Layer: Convolutional Transpose
        u8 = keras.layers.Conv2DTranspose(32, (2, 2), strides=(2, 2), padding='same')(c7)
        u8 = keras.layers.concatenate([u8, c2])
        c8 = keras.layers.Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(u8)
        c8 = keras.layers.Dropout(0.1)(c8)
        c8 = keras.layers.Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c8)
        # Nineth Layer: Convolutional Transpose
        u9 = keras.layers.Conv2DTranspose(16, (2, 2), strides=(2, 2), padding='same')(c8)
        u9 = keras.layers.concatenate([u9, c1], axis=3)
        c9 = keras.layers.Conv2D(16, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(u9)
        c9 = keras.layers.Dropout(0.1)(c9)
        c9 = keras.layers.Conv2D(16, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c9)
        # Outout Layer
        outputDec = keras.layers.Conv2D(1, (1, 1), activation='sigmoid', name='seg')(c9)

        # Classification Layer
        flat = keras.layers.Flatten()(c5)
        outputClass = keras.layers.Dense(1, activation='sigmoid', name='clf')(flat)  

        model = keras.Model(inputs=[inputs], outputs=[outputDec, outputClass])
        return model