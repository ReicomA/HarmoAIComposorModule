from deeplearningProcessor import DeepLearningProcessor

def DLprocess(modelRoot, noteSize, resultTmpRoot, useGpuValue):

    DLProcessor = DeepLearningProcessor(modelRoot, noteSize, resultTmpRoot)

    DLProcessor.makeModel()

    input_sequence = DLProcessor.makeInputSequence()
    options = DLProcessor.setConfigure(input_sequence)

    result = DLProcessor.generate(input_sequence, options)
    DLProcessor.makeFile(result)