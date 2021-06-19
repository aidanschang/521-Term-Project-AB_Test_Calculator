
class AB_test():
    """this class devotes to calculate all metrics for setting up and concluding our hypothesis test"""
    def __init__(self,__h_c,__h_v,x_c,x_v,__z):
        self.__h_control = h_c
        self.__h_variant = h_v
        self.x_control = x_c
        self.x_variant = x_v
        self.__confidence_level = __z

    def __str__(self):
        return "Declared null hypothesis at which there is no " \
               "statistically significance between control and variant.\n"\
               "Total sessions (home: {}, lander-1: {})\n" \
               "Total bounced sessions (home: {}, lander-1: {})\n" \
            .format(self.__h_control, self.__h_variant,self.x_control, self.x_variant)

    def __setting_metrics(self):
        try:
            self.control_p = self.x_control / self.__h_control
            self.variant_p = self.x_variant / self.__h_variant
            self.delta = self.control_p - self.variant_p
            self.prob_pool = (self.x_control + self.x_variant) / (self.__h_control + self.__h_variant)
            self.standard_error = (self.prob_pool * (1 - self.prob_pool) * (1 / self.__h_control + 1 / self.__h_variant)) ** .5
            if self.__confidence_level == .90:
                self.Z_SCORE = 1.645
            elif self.__confidence_level == .95:
                self.Z_SCORE = 1.96
            elif self.__confidence_level == .99:
                self.Z_SCORE = 2.576
        except ZeroDivisionError:
            print("Raw data cannot contain 0 inputs")
        except AttributeError:
            print("Raw data must be numerical numbers")

    def statistical_significance(self):
        self.__setting_metrics()
        if self.control_p > self.variant_p:
            self.__comparison = 'higher'
        else:
            self.__comparison = 'lower'
        m = self.Z_SCORE * self.standard_error
        self.confidence_level_min = self.delta - m
        self.confidence_level_max = self.delta + m
        self.test_statistic = self.delta / self.standard_error
        return "'home' bounce rate({:,.2f}%) was {:,.2f}% {} than the 'lander-1' bounce rate ({:,.2f}%)\n" \
               "Confidence Level at {:,.0f}% has Critical Z-Score of {} and Test Statistic is {:,.2f}\n". \
            format(self.control_p * 100, self.delta * 100, self.__comparison, self.variant_p * 100,
                   100 * self.__confidence_level, self.Z_SCORE, self.test_statistic)

    def __repr__(self):
        if self.test_statistic > self.Z_SCORE:
            return 'Since the Test Statistic({:,.2f}) is higher than Critical Z-Score({});\n' \
                   'reject null hypothesis, test is statistically significant.'.\
                format(self.test_statistic,self.Z_SCORE)
        elif self.test_statistic < self.Z_SCORE:
            return 'Since the Test Statistic({:,.2f}) is lower than Critical Z-Score(-{});\n' \
                   'reject null hypothesis, test has negative impact.'.\
                format(self.test_statistic,-self.Z_SCORE)
        else:
            return 'Since the Test Statistic({}) is within Critical Z-Score(-{} to {});\n'\
                   'accept null hypothesis, the test did not showed significant difference.'.\
                  format(self.test_statistic,self.Z_SCORE, self.Z_SCORE)

if __name__ == '__main__':
    """Since every csv files' format will be slightly different from one another, 
    I cleaned the file under name-main block instead cleaning the file within a class"""
    import os
    import csv
    os.chdir(r'C:\Users\Aidan\PycharmProjects\HelloWorld')
    ab_test_csv= open('ab_test.csv', 'r')
    #creating dictionaries for landing sessions and bounced sessions
    landing_sessions = {}
    bounced_sessions = {}
    # using for loop to iterate each line from ab_test_csv
    for line in ab_test_csv:
        landing_page = line.split(',')[1]
        pageview_count = line.split(',')[2][:-1]
        #calculate total sessions
        landing_sessions[landing_page] = landing_sessions.get(landing_page, 0) + 1
        #calculate total bounced sessions
        if landing_page == '/home' and pageview_count == '1':
            bounced_sessions['home_bounced'] = bounced_sessions.get('home_bounced', 0) + 1
        elif landing_page == '/lander-1' and pageview_count == '1':
            bounced_sessions['lander_bounced'] = bounced_sessions.get('lander_bounced', 0) + 1
    #assigning values to the attributes of ab_test
    h_c = landing_sessions['/home']
    h_v = landing_sessions['/lander-1']
    x_c = bounced_sessions['home_bounced']
    x_v = bounced_sessions['lander_bounced']
    confident_percent= 0.95


    #execute the class and methods
    final_project = AB_test(h_c,h_v,x_c,x_v,confident_percent)
    print(final_project)
    print(final_project.statistical_significance())
    print(final_project.__repr__())
    #unit testing using assert statements
    assert final_project.control_p == x_c / h_c, "probability for control has error!"
    assert final_project.variant_p == x_v / h_v, "probability for variant has error!"
    assert final_project.delta == x_c / h_c - x_v / h_v, "probability delta has error!"
    assert final_project.prob_pool == (x_c + x_v) / (h_c + h_v), "probability pool has error!"
    assert final_project.standard_error ==(((x_c + x_v) / (h_c + h_v)) * (1 - ((x_c + x_v) /
                            (h_c + h_v))) * (1 / h_c + 1 / h_v)) ** .5,"standard_error has error!"
    assert final_project.test_statistic ==\
           (x_c / h_c - x_v / h_v) / ((((x_c + x_v) / (h_c + h_v)) * (1 - ((x_c + x_v) /
            (h_c + h_v))) * (1 / h_c + 1 / h_v)) ** .5), "test statistic has error!"