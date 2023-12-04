clear;

% Read in text file with file paths
test_data = readlines('test_audio.txt',"EmptyLineRule","skip");
train_data = readlines('train_audio.txt',"EmptyLineRule","skip");

% For each file path, extract some features
relpath = "../../";
resamp_rate = 22050;
num_features = 499;
specCentroid = zeros(length(test_data),num_features);
specSpread = zeros(length(test_data),num_features);
pitch = zeros(length(test_data),num_features);
for i=1:length(test_data)
    % Read in audio file
    clear audio rate features;
    [audio, rate] = audioread(strcat(relpath,test_data(i)));

    % Resample to 22.5kHz
    if rate ~= 22050
        [Numer, Denom] = rat(resamp_rate/rate);
        audio_resampled = resample(audio, Numer, Denom);
    end
        
    % Set up feature extractor
    aFE = audioFeatureExtractor( ...
        SampleRate=resamp_rate, ...
        Window=hamming(round(0.03*resamp_rate),"periodic"), ...
        OverlapLength=round(0.01*resamp_rate), ...
        spectralCentroid=true, ...
        spectralSpread=true, ...
        pitch=true);
    
    % Extract features on Mono channel
    features = extract(aFE,audio_resampled(:,1));
    specCentroid(i,:) = features(:,1)';
    specSpread(i,:) = features(:,2)';
    pitch(i,:) = features(:,3)';
end